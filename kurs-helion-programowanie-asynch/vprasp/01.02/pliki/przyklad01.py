# synchronous

import requests
from time import time


def get_len_of_google_response():
    length = 0
    sites = ['https://google.com', 'https://morsecode.world', 'https://helion.pl', 'https://videopoint.pl',
             'https://pl.wikipedia.org', 'https://hardpuzzle.org', 'https://www.chess.com',
             'https://www.youtube.com']
    for URL in sites:
        r = requests.get(URL)
        html_data = r.text
        length += len(html_data)
    return length


def get_two_hundredth_prime():
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
    return to_return


start = time()
my_length = get_len_of_google_response()
my_prime = get_two_hundredth_prime()
print(my_length, my_prime, flush=True)
stop = time()
print(stop - start, flush=True)

# 11.5 +/- 1s
