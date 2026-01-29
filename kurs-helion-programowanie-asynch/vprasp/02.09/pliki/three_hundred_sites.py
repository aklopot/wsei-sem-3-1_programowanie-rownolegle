import aiohttp
import asyncio
from time import time

sites = ['https://google.com', 'https://pl.wikipedia.org', 'https://www.youtube.com'] * 100


async def get_url(url, session):
    getter = await session.get(url)
    return await getter.text()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        length = 0
        for site in sites:
            tasks.append(asyncio.create_task(get_url(site, session)))
        for task in tasks:
            result = await task
            length += len(result)
        print(length)

start = time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
stop = time()
print(f"{stop-start}s")

# 4.07
# 3.14
