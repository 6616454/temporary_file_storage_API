from sqlalchemy import delete

from celery_app import app
from database import async_session
import tables
import asyncio


async def time_to_delete2(file_id: int):
    session = async_session()
    await session.execute(delete(tables.File).filter_by(id=file_id))
    await session.commit()
    await session.close()


@app.task
def time_to_delete(file_id: int):
    asyncio.run(time_to_delete2(file_id))
