import requests
from multiprocessing.pool import Pool, ThreadPool
from time import time


def get_response_for_url(url):
    r = requests.get(url)
    html_data = r.text
    return html_data


if __name__ == "__main__":
    sites = ['https://google.com', 'https://pl.wikipedia.org', 'https://www.youtube.com'] * 100
    start = time()
    p = ThreadPool(8)
    with p:
        values = p.map(get_response_for_url, sites)
    stop = time()
    print(stop - start)

# 24.77
# 24.46
