"""
Pełny benchmark wszystkich metod z zadań 1, 2 i 3.
Uruchamia sekwencyjne sumowanie, threading.Thread, multiprocessing.Pool,
Parallel.For (ProcessPoolExecutor) oraz Parallel.ForEach na 4 plikach CSV.
Wyniki zapisuje do pliku logu.
"""

import os
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool

from src.modules.csv_loader import load_numbers_from_csv

DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'dane_wejsciowe'
)
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
CSV_FILES = ['numbers1.csv', 'numbers2.csv', 'numbers3.csv', 'numbers4.csv']


# ---- Funkcje robocze (poziom modułu, wymagane przez multiprocessing) ----

def _sum_chunk(chunk):
    """Sumuje fragment tablicy."""
    total = 0
    for num in chunk:
        total += num
    return total


def _process_csv_file(filepath):
    """Wczytuje plik CSV i zwraca sumę."""
    abs_path = os.path.abspath(filepath)
    with open(abs_path, 'r') as f:
        content = f.read().strip()
    numbers = [int(x) for x in content.split(';') if x.strip()]
    return {'file': os.path.basename(filepath), 'count': len(numbers), 'sum': sum(numbers)}


class BenchmarkRunner:
    """
    Uruchamia pełny benchmark metod z zadań 1-3 i zapisuje log.
    """

    def __init__(self):
        self.numbers = None

    def _load_data(self):
        """Wczytuje numbers1.csv."""
        if self.numbers is None:
            path = os.path.join(DATA_DIR, 'numbers1.csv')
            self.numbers = load_numbers_from_csv(path)

    @staticmethod
    def _split(numbers, n):
        """Dzieli tablicę na n fragmentów."""
        size = len(numbers) // n
        chunks = []
        for i in range(n):
            s = i * size
            e = s + size if i < n - 1 else len(numbers)
            chunks.append(numbers[s:e])
        return chunks

    # ---- Metody sumowania ----

    @staticmethod
    def _seq_sum(numbers):
        total = 0
        for num in numbers:
            total += num
        return total

    @staticmethod
    def _partial_sum(numbers, start, end, results, idx):
        total = 0
        for i in range(start, end):
            total += numbers[i]
        results[idx] = total

    def _thread_sum(self, numbers, num_threads):
        """Sumowanie z threading.Thread."""
        n = len(numbers)
        chunk_size = n // num_threads
        threads = []
        results = [0] * num_threads
        for i in range(num_threads):
            s = i * chunk_size
            e = s + chunk_size if i < num_threads - 1 else n
            t = threading.Thread(target=self._partial_sum, args=(numbers, s, e, results, i))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return sum(results)

    def _pool_sum(self, numbers, num_procs):
        """Sumowanie z multiprocessing.Pool."""
        chunks = self._split(numbers, num_procs)
        with Pool(processes=num_procs) as pool:
            partial = pool.map(_sum_chunk, chunks)
        return sum(partial)

    def _executor_sum(self, numbers, num_workers):
        """Sumowanie z ProcessPoolExecutor (Parallel.For)."""
        chunks = self._split(numbers, num_workers)
        with ProcessPoolExecutor(max_workers=num_workers) as ex:
            partial = list(ex.map(_sum_chunk, chunks))
        return sum(partial)

    # ---- Benchmark ----

    def run(self):
        """Uruchamia pełny benchmark i zapisuje log."""
        self._load_data()
        numbers = self.numbers
        file_paths = [os.path.join(DATA_DIR, f) for f in CSV_FILES]
        log_path = os.path.join(LOG_DIR, 'benchmark_log.txt')

        print("\n" + "=" * 60)
        print("  PEŁNY BENCHMARK — METODY Z ZADAŃ 1, 2 I 3")
        print("=" * 60)

        results = []

        def bench(name, func):
            start = time.perf_counter()
            result = func()
            elapsed = (time.perf_counter() - start) * 1000
            results.append({'nazwa': name, 'suma': result, 'czas_ms': elapsed})
            print(f"  {name:<45} suma: {result:>10}, czas: {elapsed:>10.4f} ms")
            return elapsed

        print("\n  --- Sumowanie numbers1.csv (10 000 elementów) ---\n")

        # Zadanie 1
        bench("Sekwencyjna", lambda: self._seq_sum(numbers))
        bench("threading.Thread (2 wątki)", lambda: self._thread_sum(numbers, 2))
        bench("threading.Thread (4 wątki)", lambda: self._thread_sum(numbers, 4))
        bench("threading.Thread (8 wątków)", lambda: self._thread_sum(numbers, 8))
        bench("multiprocessing.Pool (2 procesy)", lambda: self._pool_sum(numbers, 2))
        bench("multiprocessing.Pool (4 procesy)", lambda: self._pool_sum(numbers, 4))
        bench("multiprocessing.Pool (8 procesów)", lambda: self._pool_sum(numbers, 8))

        # Zadanie 3 — Parallel.For
        bench("Parallel.For / Executor (4 workery)", lambda: self._executor_sum(numbers, 4))
        bench("Parallel.For / Executor (8 workerów)", lambda: self._executor_sum(numbers, 8))

        # Zadanie 3 — Parallel.ForEach
        print(f"\n  --- Parallel.ForEach — przetwarzanie 4 plików CSV ---\n")

        start = time.perf_counter()
        seq_file_results = [_process_csv_file(fp) for fp in file_paths]
        seq_files_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=4) as ex:
            par_file_results = list(ex.map(_process_csv_file, file_paths))
        par_files_time = (time.perf_counter() - start) * 1000

        print(f"  {'Sekwencyjne przetwarzanie plików':<45} czas: {seq_files_time:>10.4f} ms")
        for r in seq_file_results:
            print(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}")

        print(f"\n  {'Parallel.ForEach (4 pliki równolegle)':<45} czas: {par_files_time:>10.4f} ms")
        for r in par_file_results:
            print(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}")

        # Zapis logu
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("=" * 60 + "\n")
            log.write("  BENCHMARK — PODSUMOWANIE METOD Z ZADAŃ 1, 2 I 3\n")
            log.write("=" * 60 + "\n\n")

            log.write("--- Sumowanie numbers1.csv ---\n\n")
            log.write(f"  {'Metoda':<45} {'Suma':>10}   {'Czas [ms]':>12}\n")
            log.write(f"  {'-'*45} {'-'*10}   {'-'*12}\n")
            for r in results:
                log.write(f"  {r['nazwa']:<45} {r['suma']:>10}   {r['czas_ms']:>12.4f}\n")

            log.write(f"\n--- Parallel.ForEach — 4 pliki CSV ---\n\n")
            log.write(f"  Sekwencyjnie: {seq_files_time:.4f} ms\n")
            for r in seq_file_results:
                log.write(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}\n")
            log.write(f"\n  Parallel.ForEach: {par_files_time:.4f} ms\n")
            for r in par_file_results:
                log.write(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}\n")

            log.write(f"\n{'='*60}\n")

        print(f"\n  Log zapisany do: benchmark_log.txt")
