import aiofiles
from aiohttp import ClientSession
from fastapi import UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from zipstream import AioZipStream

from auth.schemas import User
from database import get_session

import tables
from do_rar.schemas import UpdateFile
from requests import get_request_session
from settings import settings

from .tasks import deletion_by_time


# class LinkShortener:
#     URL = 'https://goo.su/api/links/create'
#
#     HEADERS = {
#         'x-goo-api-token': settings.token_api
#     }
#
#     PAYLOAD = {}
#
#     # def __init__(self, request_session: ClientSession = Depends(get_request_session)):
#     #     self.request_session = request_session
#
#     async def get_file_link(self, file_id: int):
#         link = f'{settings.main_link}{file_id}'
#         self.PAYLOAD['url'] = link
#
#     async def create_short_link(self, file_id: int):
#         await self.get_file_link(file_id)
#
#         async with self.request_session.post(
#                 url=self.URL,
#                 headers=self.HEADERS,
#                 data=self.PAYLOAD
#         ) as response:
#             data = await response.json()
#
#         return data['short_url']


class RarService:
    URL = 'https://goo.su/api/links/create'

    HEADERS = {
        'x-goo-api-token': settings.token_api
    }

    PAYLOAD = {}

    def __init__(self, session: AsyncSession = Depends(get_session),
                 request_session: ClientSession = Depends(get_request_session)):
        self.request_session = request_session
        self.session = session

    async def get_file_link(self, file_id: int):
        link = f'{settings.main_link}{file_id}'
        print(link)
        self.PAYLOAD['url'] = link

    async def create_short_link(self, file_id: int):
        await self.get_file_link(file_id)

        async with self.request_session.post(
                url=self.URL,
                headers=self.HEADERS,
                data=self.PAYLOAD
        ) as response:
            data = await response.json()

        print(data['short_url'])

        return data['short_url']

    @staticmethod
    async def dict_files(files: list[UploadFile]) -> list[dict[str, str]]:
        """Function for create list of dicts with key: 'file' value: 'path to file' """
        upload_files = []

        for file in files:
            async with aiofiles.open(file.filename, 'wb') as buffer:
                data = await file.read()
                await buffer.write(data)
                upload_files.append({'file': f'{buffer.name}'})

        return upload_files

    @staticmethod
    async def get_file_response(file_path: str, filename: str):
        return FileResponse(
            file_path,
            headers={
                'Content-Disposition': f'attachment; filename={filename}.rar'
            }
        )

    async def _get_file(self, file_id: int, user_id: int = None) -> tables.File:
        if not user_id:
            output_file = await self.session.execute(select(tables.File).filter_by(id=file_id))
        else:
            output_file = await self.session.execute(select(tables.File).filter_by(id=file_id, user_id=user_id))

        output_file = output_file.scalars().first()

        if output_file:
            return output_file

        raise HTTPException(
            status_code=404,
            detail='The file does not exist or public access to the file is not allowed'
        )

        # HTTPException

    async def _update_file(self, file_id: int, user_id: int, **kwargs):
        await self.session.execute(
            update(tables.File).filter_by(id=file_id, user_id=user_id).values(**kwargs)
        )

        return await self.session.commit()

    async def _delete_file(self, file_id: int, user_id: int):
        await self.session.execute(delete(tables.File).filter_by(id=file_id, user_id=user_id))

        return await self.session.commit()

    async def upload_archive_files(
            self,
            files: list[UploadFile],
            name_archive: str,
            user: User
    ) -> tables.File:
        """Function for upload and archive files"""

        path = f'{user.user_path}/{name_archive}.rar'

        rar_stream = AioZipStream(await self.dict_files(files))
        async with aiofiles.open(path, mode='wb') as rar_file:
            async for chunk in rar_stream.stream():
                await rar_file.write(chunk)

        new_file = tables.File(
            name=name_archive,
            file=path,
            link='',
            user_id=user.id,
        )

        self.session.add(new_file)
        await self.session.commit()
        await self.session.refresh(new_file)

        new_file.link = await self.create_short_link(new_file.id)

        await self.session.commit()
        await self.session.refresh(new_file)

        deletion_by_time.apply_async((new_file.id,), countdown=15)

        return new_file

    async def get_archive(
            self,
            file_id: int,
            user: User
    ):
        output_file = await self._get_file(file_id)

        if output_file.public:
            return await self.get_file_response(output_file.file, output_file.name)

        output_file = await self._get_file(file_id, user.id)

        return await self.get_file_response(output_file.file, output_file.name)

    async def update_file_info(
            self,
            file_id: int,
            user_id: int,
            file_info: UpdateFile,
    ):
        file = await self._get_file(file_id, user_id)

        file_data = UpdateFile(
            name=file.name,
            public=file.public
        )

        new_data = file_info.dict(exclude_unset=True)

        updated_file_data = file_data.copy(update=new_data)

        await self._update_file(file_id, user_id, **updated_file_data.dict())

    async def delete_file(self, file_id: int, user_id: int):
        await self._delete_file(file_id, user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
