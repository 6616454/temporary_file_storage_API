import aiohttp
from aiohttp import ClientSession


async def get_request_session() -> ClientSession:
    async with aiohttp.ClientSession() as session:
        yield session
