import asyncio
from random import randint


async def f(a, b, some_dict: dict):
    await asyncio.sleep(0.1)
    some_dict[f'{a}+{b}'] = a+b
    return randint(0, 1)


async def main():
    zero_task = list(asyncio.all_tasks())[0]
    results = dict()
    for r in range(1, 100):
        asyncio.create_task(f(r, r+1, results))
    tasks = asyncio.all_tasks() - {zero_task}
    returns = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)
    print(returns)

asyncio.run(main())
