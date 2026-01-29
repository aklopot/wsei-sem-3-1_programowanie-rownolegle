import asyncio


async def other_f(text):
    await asyncio.sleep(2)
    print(text)


async def main():
    task = asyncio.create_task(other_f("nie jestem main"))
    print("jestem main")
    # try:
    #     task.cancel()
    #     await task
    # except asyncio.exceptions.CancelledError:
    #     print(1)
    await task
    print("tej informacji")


asyncio.run(main())
