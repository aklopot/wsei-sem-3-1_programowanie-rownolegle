import asyncio
from asyncio import Task


async def f():
    await asyncio.sleep(0.1)
    print('done')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = [f() for i in range(10)]
    loop.run_until_complete(asyncio.gather(*task))

