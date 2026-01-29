import asyncio
from asyncio import Task


async def other_f(text, *, sleep_time):
    await asyncio.sleep(sleep_time)
    print(text)


async def main():
    task1 = asyncio.create_task(other_f("task1", sleep_time=2))
    task2 = asyncio.create_task(other_f("task2", sleep_time=1))
    task3 = asyncio.create_task(other_f("task3", sleep_time=3))
    task4 = asyncio.create_task(other_f("task4", sleep_time=5))
    task5 = asyncio.create_task(other_f("task5", sleep_time=1))
    print("jestem main")
    a_list = [task1, task2, task3, task4, task5]
    await asyncio.gather(*a_list, return_exceptions=True)
    print("tej informacji")


asyncio.run(main())
