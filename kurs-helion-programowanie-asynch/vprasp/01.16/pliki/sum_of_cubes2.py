# Znaleźć całkowite liczby a, b i c, które w sumie trzecich potęg a^3 + b^3 + c^3 dadzą liczbę całkowitą k
from time import time
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def f(a, k_dict):
    if a % 10 == 0:
        print(a)
    for b in range(a, 1000):
        for c in range(b, 1000):
            result = a**3 + b**3 + c**3
            if 0 <= result <= 100 and result not in k_dict.keys():
                k_dict[result] = f"{a}^3 + {b}^3 + {c}^3 ({a**3} + {b**3} + {c**3}) = {result}"


if __name__ == "__main__":
    start = time()
    k = Manager().dict()

    with ProcessPoolExecutor(max_workers=16) as executor:
        execs = []
        for a in range(-1000, 5):
            execs.append(executor.submit(f, a, k))
        for element in execs:
            element.result()

    for key, value in k.items():
        print(value)
    print(sorted(list(k.keys())))
    print(len(k.keys()))
    print(f"{100*len(k.keys())/101}%")

    stop = time()
    print(f"{stop - start}s")

# Szeregowo: < 2 minuty (115.98), 69
# Równolegle 4-procesy (starmap): 28s, 69
# Równolegle 4-procesy (patial): 28s, 69
# Równolegle 8-procesów (patial): 16.5s, 69
# Równolegle 16-procesów (patial): 11.12s, 69
# Równolegle 8-procesów (patial), do 1000: 142s, 70
# Równolegle 16-procesów (patial), do 1000: 149s, 70
# Równolegle 16-procesów (concurrent.futures), do 1000: 118s, 70
# k=42 (a = -80538738812075974, b = 80435758145817515, c = 12602123297335631)
