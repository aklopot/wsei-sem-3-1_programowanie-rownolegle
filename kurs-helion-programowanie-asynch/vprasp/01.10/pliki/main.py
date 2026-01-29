from multiprocessing import Pool
from time import sleep, time


def first(some_list, limit):
    summary = 0
    for i in range(limit + 1):
        summary += i
        sleep(0.001)
    some_list.append(summary)


def first2(limit):
    summary = 0
    for i in range(limit + 1):
        summary += i
    return summary


if __name__ == "__main__":
    start = time()
    a_list = [100*i for i in range(1, 21)]
    p = Pool(5)
    with p:
        value = p.map(first2, a_list)
        print(value)
    stop = time()

    print(stop - start)

