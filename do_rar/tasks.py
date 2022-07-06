import os
from uuid import UUID

from sqlalchemy import select

from celery_app import app
from database import async_session
import tables
import asyncio


async def async_deletion_by_time(file_id: UUID):
    session = async_session()

    file_object = await session.execute(select(tables.File).filter_by(id=file_id))

    file = file_object.scalars().first()

    os.remove(file.file)

    await session.delete(file)
    await session.commit()
    await session.close()


@app.task
def deletion_by_time(file_id: UUID):
    # asyncio.run(async_deletion_by_time(file_id))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_deletion_by_time(file_id))


@app.task
def clear_temp_files(upload_files: list[dict]):
    for temp_file in upload_files:
        os.remove(temp_file['file'])
