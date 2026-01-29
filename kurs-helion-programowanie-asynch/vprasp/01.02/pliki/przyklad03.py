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
    primes = [2]
    how_many_primes = 1
    for i in range(3, 10**7, 2):
        is_prime = True
        sqrt_i = int(i**0.5)
        for prime in primes:
            if prime > sqrt_i:
                break
            if i % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
            how_many_primes += 1
            if how_many_primes == 2*10**5:
                break
    return primes[-1]


start = time()
my_length = get_len_of_google_response()
my_prime = get_two_hundredth_prime()
print(my_length, my_prime)
stop = time()
print(stop - start)

# 7.5s +/- 0.5s
