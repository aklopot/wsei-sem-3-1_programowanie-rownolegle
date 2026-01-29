from multiprocessing import Process, Manager
import asyncio_and_multiprocessing_util

if __name__ == "__main__":
    my_shared_dict = Manager().dict()

    processes = []

    for i in range(8):
        p = Process(target=getattr(asyncio_and_multiprocessing_util, f"task{i+1}"), args=(my_shared_dict, ))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    for key, value in my_shared_dict.items():
        print(value)
    print(sorted(list(my_shared_dict.keys())))
    print(len(my_shared_dict.keys()))
    print(f"{100*len(my_shared_dict.keys())/101}%")
