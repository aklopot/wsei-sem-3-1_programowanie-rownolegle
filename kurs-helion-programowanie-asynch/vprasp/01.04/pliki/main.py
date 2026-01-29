from multiprocessing import Process
from time import sleep, time


def first():
    summary = 0
    for i in range(1001):
        summary += i
        sleep(0.005)
    return summary


def second():
    product = 1
    for i in range(1, 1001):
        product *= 1
        sleep(0.001)
    return product


def third():
    big_number = 10**100
    for _ in range(100):
        big_number = big_number ** 0.5
        sleep(0.01)
    return big_number


# start = time()
# first()
# second()
# third()
# stop = time()
# print(stop - start)


if __name__ == "__main__":
    start = time()
    p1 = Process(target=first)
    p2 = Process(target=second)
    p3 = Process(target=third)
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    stop = time()
    print(stop - start)

# 33.46s -- synchronous
# 16.02 -- asynchronous
