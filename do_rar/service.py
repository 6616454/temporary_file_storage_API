import aiofiles
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from zipstream import AioZipStream


class RarService:

    @staticmethod
    async def dict_files(files: list[UploadFile]) -> list[dict[str, str]]:
        upload_files = []

        for file in files:
            async with aiofiles.open(file.filename, 'wb') as buffer:
                data = await file.read()
                await buffer.write(data)
                upload_files.append({'file': f'{buffer.name}'})

        return upload_files

    async def archive_files(
            self,
            files: list[UploadFile],
            name_archive: str
    ):
        rar_stream = AioZipStream(await self.dict_files(files))
        async with aiofiles.open(f'{name_archive}.rar', mode='wb') as rar_file:
            async for chunk in rar_stream.stream():
                await rar_file.write(chunk)

        return FileResponse(
            rar_file.name,  # Путь до файла
            headers={
                'Content-Disposition': f'attachment; filename={rar_file.name}'
            }
        )
