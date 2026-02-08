"""
Kalkulator sumy z użyciem multiprocessing.Pool.
Porównanie sumowania sekwencyjnego z wieloprocesowym.
Uwaga: multiprocessing omija GIL — realna równoległość,
ale narzut tworzenia procesów dominuje przy małym zadaniu.
"""

import os
import time
from multiprocessing import Pool

from src.modules.csv_loader import load_numbers_from_csv


def _worker_sum(chunk):
    """Funkcja robocza procesu — sumuje fragment tablicy liczb."""
    total = 0
    for num in chunk:
        total += num
    return total


class MultiprocessSumCalculator:
    """
    Oblicza sumę liczb metodami:
    - sekwencyjną
    - multiprocessing.Pool z 2 i 8 procesami
    """

    DATA_FILE = os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'dane_wejsciowe', 'numbers1.csv'
    )

    def __init__(self):
        self.numbers = None

    def _load_data(self):
        """Wczytuje dane z CSV, jeśli jeszcze nie wczytano."""
        if self.numbers is None:
            self.numbers = load_numbers_from_csv(self.DATA_FILE)
            print(f"  Wczytano {len(self.numbers)} liczb z pliku CSV.")

    @staticmethod
    def _sequential_sum(numbers):
        """Oblicza sumę sekwencyjnie."""
        total = 0
        for num in numbers:
            total += num
        return total

    @staticmethod
    def _split_into_chunks(numbers, num_chunks):
        """Dzieli listę na w przybliżeniu równe fragmenty."""
        n = len(numbers)
        chunk_size = n // num_chunks
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else n
            chunks.append(numbers[start:end])
        return chunks

    def _multiprocess_sum(self, numbers, num_processes):
        """Oblicza sumę z użyciem multiprocessing.Pool dla podanej liczby procesów."""
        chunks = self._split_into_chunks(numbers, num_processes)
        with Pool(processes=num_processes) as pool:
            partial_sums = pool.map(_worker_sum, chunks)
        return sum(partial_sums)

    def run(self):
        """Uruchamia porównanie: sekwencyjne vs multiprocessing.Pool (2, 8 procesów)."""
        self._load_data()
        numbers = self.numbers

        print("\n" + "-"*60)
        print("  Wersja 2: multiprocessing.Pool (bez GIL - zysk)")
        print("-"*60)

        # Sekwencyjnie
        start = time.perf_counter()
        seq_sum = self._sequential_sum(numbers)
        seq_time = (time.perf_counter() - start) * 1000

        # 2 procesy
        start = time.perf_counter()
        p2_sum = self._multiprocess_sum(numbers, 2)
        p2_time = (time.perf_counter() - start) * 1000

        # 8 procesów
        start = time.perf_counter()
        p8_sum = self._multiprocess_sum(numbers, 8)
        p8_time = (time.perf_counter() - start) * 1000

        print(f"  Metoda sekwencyjna              – suma: {seq_sum}, czas wykonania: {seq_time:.4f} ms")
        print(f"  Metoda wieloprocesowa (2 proc.) – suma: {p2_sum}, czas wykonania: {p2_time:.4f} ms")
        print(f"  Metoda wieloprocesowa (8 proc.) – suma: {p8_sum}, czas wykonania: {p8_time:.4f} ms")

        print("\n  [INFO] multiprocessing.Pool omija GIL — realna równoległość, ale narzut")
        print("         tworzenia procesów dominuje przy tak małym zadaniu (~0.3 ms pracy).")
