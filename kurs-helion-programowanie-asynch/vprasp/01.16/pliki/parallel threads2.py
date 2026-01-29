from matplotlib import pyplot as plt
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
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
    values = []

    # ===1===
    # with ThreadPoolExecutor(max_workers=8) as executor:
    #     execs = []
    #     for i in range(1, 8+1):
    #         execs.append(executor.submit(working_times, i))
    #     for element in execs:
    #         values.append(element.result())

    # ===2===
    a_list = [i + 1 for i in range(8)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        values = executor.map(working_times, a_list)

    segments = []
    colors = ['red', 'green', 'blue', 'yellow', 'black', 'orange', 'silver', 'purple']
    for i, value_list in enumerate(values):
        for value in value_list:
            x, y = [value[0], value[1]], [i, i]
            segments += [x, y, colors[i]]
    plt.plot(*segments)
    plt.show()
