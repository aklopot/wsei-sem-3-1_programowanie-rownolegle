import asyncio


def f(a, k_dict):
    if a % 10 == 0:
        print(a)
    for b in range(a, 1500):
        for c in range(b, 2000):
            if a+b+2*c < 0:
                continue
            result = a**3 + b**3 + c**3
            if 0 <= result <= 100 and result not in k_dict.keys():
                k_dict[result] = f"{a}^3 + {b}^3 + {c}^3 ({a**3} + {b**3} + {c**3}) = {result}"


def task1(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async1(shared_dict)))


def task2(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async2(shared_dict)))


def task3(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async3(shared_dict)))


def task4(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async4(shared_dict)))


def task5(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async5(shared_dict)))


def task6(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async6(shared_dict)))


def task7(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async7(shared_dict)))


def task8(shared_dict):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(async8(shared_dict)))


async def async1(shared_dict):
    for a in range(-500, -440):
        f(a, shared_dict)


async def async2(shared_dict):
    for a in range(-440, -380):
        f(a, shared_dict)


async def async3(shared_dict):
    for a in range(-380, -320):
        f(a, shared_dict)


async def async4(shared_dict):
    for a in range(-320, -260):
        f(a, shared_dict)


async def async5(shared_dict):
    for a in range(-260, -200):
        f(a, shared_dict)


async def async6(shared_dict):
    for a in range(-200, -140):
        f(a, shared_dict)


async def async7(shared_dict):
    for a in range(-140, 70):
        f(a, shared_dict)


async def async8(shared_dict):
    for a in range(-70, 5):
        f(a, shared_dict)
