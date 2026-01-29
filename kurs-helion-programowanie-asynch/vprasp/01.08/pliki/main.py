from multiprocessing import Process, Manager
from time import sleep, time


def first(some_list, limit):
    summary = 0
    for i in range(limit + 1):
        summary += i
        sleep(0.001)
    some_list.append(summary)


if __name__ == "__main__":
    my_manager = Manager()
    my_list = my_manager.list()
    start = time()
    a_list = [100*i for i in range(1, 70)]
    processes = [Process(target=first, args=(my_list, x)) for x in a_list]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    stop = time()

    print(my_list)
    print(stop - start)

# 33.46s -- synchronous
# 16.02 -- asynchronous
