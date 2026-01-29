from matplotlib import pyplot as plt
from multiprocessing.pool import Pool, ThreadPool
from time import sleep, time
global_start = time()


def working_times(number):
    print(f"number: {number}")
    list_of_times = []
    for _ in range(10**2):
        sleep(0.001)
        start = time()
        some_number = 6**7**6
        stop = time()
        x1 = start - global_start
        x2 = start - global_start + start - stop
        list_of_times.append([x1, x2])
    return list_of_times


if __name__ == "__main__":
    a_list = [i+1 for i in range(8)]
    values = []
    for element in a_list:
        values.append(working_times(element))

    segments = []
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'orange', 'silver', 'purple']
    for i, value_list in enumerate(values):
        for value in value_list:
            x, y = [value[0], value[1]], [i, i]
            segments += [x, y, colors[i]]
    plt.plot(*segments)
    plt.show()
