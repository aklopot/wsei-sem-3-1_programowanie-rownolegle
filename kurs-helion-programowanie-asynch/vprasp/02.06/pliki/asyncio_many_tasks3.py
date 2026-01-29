import asyncio
from asyncio import Task


async def other_f(text, *, sleep_time):
    await asyncio.sleep(sleep_time)
    print(text)


async def main():
    sleeps = [2, 1, 3, 5, 1]
    zero_task = list(asyncio.all_tasks())[0]
    for i, sleep_t in enumerate(sleeps):
        asyncio.create_task(other_f(f"task{i+1}", sleep_time=sleep_t))
    print("jestem main")
    pending = asyncio.all_tasks() - {zero_task}
    group = asyncio.gather(*pending, return_exceptions=True)
    await group
    print("tej informacji")


asyncio.run(main())
