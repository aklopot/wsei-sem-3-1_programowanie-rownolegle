import asyncio
from asyncio import Task


async def other_f(text, *, sleep_time):
    await asyncio.sleep(sleep_time)
    print(text)


async def main():
    sleeps = [2, 1, 3, 5, 1]
    tasks = []
    for i, sleep_t in enumerate(sleeps):
        tasks.append(asyncio.create_task(other_f(f"task{i+1}", sleep_time=sleep_t)))
    print("jestem main")
    for task in tasks:
        await task
    print("tej informacji")


asyncio.run(main())
