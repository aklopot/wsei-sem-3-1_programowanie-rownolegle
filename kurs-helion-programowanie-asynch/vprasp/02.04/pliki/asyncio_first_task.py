import asyncio
from asyncio import Task


async def other_f(text):
    await asyncio.sleep(2)
    print(text)


async def main():
    # task = asyncio.ensure_future(other_f("nie jestem main"))
    # task2 = asyncio.ensure_future(task)
    # print(type(task))
    # print(task is task2)
    task = asyncio.create_task(other_f("nie jestem main"))
    print("jestem main")
    await task
    print("tej informacji")


asyncio.run(main())
