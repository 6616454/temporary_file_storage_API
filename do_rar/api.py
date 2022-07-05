from fastapi import APIRouter, UploadFile, File, Depends

from auth.schemas import User
from auth.service import get_current_user
from do_rar.schemas import OutputFile, UpdateFile

from do_rar.service import RarService

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


@router.get('/{file_id}')
async def get_file(
        file_id: int,
        service: RarService = Depends(),
        user: User = Depends(get_current_user)
):
    """Endpoint to get files"""
    return await service.get_archive(file_id, user)


@router.post('/', response_model=OutputFile)
async def upload_files(
        name_archive: str,
        files: list[UploadFile] = File(...),
        service: RarService = Depends(),
        user: User = Depends(get_current_user)
):
    """Endpoint to upload files"""
    return await service.upload_archive_files(files=files, name_archive=name_archive, user=user)


@router.patch('/{file_id}')
async def update_file(
        file_id: int,
        file_info: UpdateFile,
        service: RarService = Depends(),
        user: User = Depends(get_current_user)
):
    """Endpoint to update the public status of file """
    return await service.update_file_info(file_id, user.id, file_info)


@router.delete('/{file_id}')
async def delete_file(
        file_id: int,
        service: RarService = Depends(),
        user: User = Depends(get_current_user)
):
    """Endpoint to delete file"""
    return await service.delete_file(file_id, user.id)
