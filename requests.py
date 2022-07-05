import asyncio

import aiohttp
from aiohttp import ClientSession
from settings import settings


async def get_request_session() -> ClientSession:
    async with aiohttp.ClientSession() as session:
        yield session


async def main():
    header = {
        'x-goo-api-token': settings.token_api
    }
    payload = {
        'url': 'https://vk.com/im?sel=496396388'
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://goo.su/api/links/create'
        async with session.post(url, headers=header, data=payload) as resp:
            data = await resp.json()
        print(data['short_url'])
    return data


if __name__ == '__main__':
    asyncio.run(main())
