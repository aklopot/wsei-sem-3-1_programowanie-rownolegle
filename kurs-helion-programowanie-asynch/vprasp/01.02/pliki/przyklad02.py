# asynchronous

import requests
from time import time
from multiprocessing import Process, Manager


def get_len_of_google_response(return_map):
    length = 0
    sites = ['https://google.com', 'https://morsecode.world', 'https://helion.pl', 'https://videopoint.pl',
             'https://pl.wikipedia.org', 'https://hardpuzzle.org', 'https://www.chess.com',
             'https://www.youtube.com']
    for URL in sites:
        r = requests.get(URL)
        html_data = r.text
        length += len(html_data)
    return_map["get_len_of_google_response"] = length


def get_two_hundredth_prime(return_map):
    prime = 1
    to_return = None
    for i in range(3, 10**7, 2):
        is_prime = True
        for j in range(3, int(i**0.5)+1, 2):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            prime += 1
            if prime == 2*10**5:
                to_return = i
                break
    return_map["get_two_hundredth_prime"] = to_return


if __name__ == "__main__":
    start = time()
    manager = Manager()
    return_dict = manager.dict()
    processes = [Process(target=get_len_of_google_response, args=(return_dict, )),
                 Process(target=get_two_hundredth_prime, args=(return_dict, ))]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(return_dict.values())
    stop = time()
    print(stop - start)

