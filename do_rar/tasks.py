from sqlalchemy import delete

from celery_app import app
from database import async_session
import tables
import asyncio


async def async_deletion_by_time(file_id: int):
    session = async_session()
    await session.execute(delete(tables.File).filter_by(id=file_id))
    await session.commit()
    await session.close()


@app.task
def deletion_by_time(file_id: int):
    # asyncio.run(async_deletion_by_time(file_id))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_deletion_by_time(file_id))
