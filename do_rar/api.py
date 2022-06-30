from fastapi import APIRouter, UploadFile, File, Depends

from do_rar.schemas import OutputArchive
from do_rar.service import RarService

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)


@router.post('/')
async def upload_files(
        name_archive: str,
        files: list[UploadFile] = File(...),
        service: RarService = Depends()
):
    return await service.archive_files(files=files, name_archive=name_archive)
