from multiprocessing import Manager, Process
from time import sleep, time


def first(some_list, limit):
    summary = 0
    for i in range(limit + 1):
        summary += i
    some_list.append(summary)


def first2(limit):
    summary = 0
    for i in range(limit + 1):
        summary += i
        sleep(0.001)
    return summary


if __name__ == "__main__":
    start = time()
    my_manager = Manager()
    my_list = my_manager.list()
    a_list = [100*i for i in range(1, 21)]
    for i in range((21-1)//5):
        processes = [Process(target=first, args=(my_list, x)) for x in a_list[5*i:5*i+5]]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    print(my_list)
    stop = time()

    print(stop - start)

