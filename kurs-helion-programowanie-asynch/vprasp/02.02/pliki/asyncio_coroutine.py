import asyncio


async def other_f(text):
    await asyncio.sleep(2)
    print(text)


async def main():
    await other_f("nie jestem main")
    print("jestem main")


asyncio.run(main())
