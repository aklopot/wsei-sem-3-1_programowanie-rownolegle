import asyncio
from random import randint
from asyncio import Task


async def other_f(text, *, sleep_time):
    await asyncio.sleep(sleep_time)
    print(text)


async def main():
    sleeps = [2, 1, 3, randint(3, 6), 1]
    tasks = []
    for i, sleep_t in enumerate(sleeps):
        tasks.append(asyncio.create_task(other_f(f"task{i+1}", sleep_time=sleep_t)))
    print("jestem main")
    try:
        await asyncio.wait_for(list(tasks)[3], 5)
    except asyncio.exceptions.TimeoutError:
        print("Task wykonywał się zbyt długo")
    print("tej informacji")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = [main()]
    loop.run_until_complete(asyncio.gather(*task))
