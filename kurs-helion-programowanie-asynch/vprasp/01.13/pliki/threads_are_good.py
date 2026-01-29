import requests
from multiprocessing.pool import Pool, ThreadPool
from time import time


def get_response_for_url(url):
    r = requests.get(url)
    html_data = r.text
    return html_data


if __name__ == "__main__":
    sites = ['https://google.com', 'https://morsecode.world', 'https://helion.pl', 'https://videopoint.pl',
             'https://pl.wikipedia.org', 'https://hardpuzzle.org', 'https://www.chess.com',
             'https://www.youtube.com']
    start = time()
    p = ThreadPool(8)
    with p:
        values = p.map(get_response_for_url, sites)
    stop = time()
    print(stop - start)

# 6.88
# 1.36
