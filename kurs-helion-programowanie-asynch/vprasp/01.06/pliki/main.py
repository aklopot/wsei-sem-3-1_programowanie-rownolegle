from multiprocessing import Process, Manager
from time import sleep, time


def first(some_list):
    summary = 0
    for i in range(1001):
        summary += i
        sleep(0.005)
    some_list.append(summary)


def second(some_list):
    product = 1
    for i in range(1, 1001):
        product *= i
        sleep(0.001)
    some_list.append(product)


def third(some_list):
    big_number = 10**100
    for _ in range(100):
        big_number = big_number ** 0.5
        sleep(0.01)
    some_list.append(big_number)


if __name__ == "__main__":
    my_manager = Manager()
    my_list = my_manager.list()
    start = time()
    p1 = Process(target=first, args=(my_list, ))
    p2 = Process(target=second, args=(my_list, ))
    p3 = Process(target=third, args=(my_list, ))
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    stop = time()
    print(my_list)
    print(stop - start)

# 33.46s -- synchronous
# 16.02 -- asynchronous
