"""
Odpowiednik Parallel.For() z TPL (C#).
W Pythonie realizowany przez concurrent.futures.ProcessPoolExecutor.

Dzieli tablicę na fragmenty i sumuje je równolegle w oddzielnych procesach.
Porównanie: sekwencyjne vs Parallel.For (4 i 8 workerów).
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor

from src.modules.csv_loader import load_numbers_from_csv


def _sum_chunk(chunk):
    """Funkcja robocza — sumuje fragment tablicy."""
    total = 0
    for num in chunk:
        total += num
    return total


class ParallelForCalculator:
    """
    Sumowanie tablicy z użyciem Parallel.For (ProcessPoolExecutor).
    Porównanie sekwencyjne vs równoległe (4 i 8 workerów).
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
        """Sumowanie sekwencyjne."""
        total = 0
        for num in numbers:
            total += num
        return total

    @staticmethod
    def _split_into_chunks(numbers, num_chunks):
        """Dzieli listę na fragmenty."""
        n = len(numbers)
        chunk_size = n // num_chunks
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else n
            chunks.append(numbers[start:end])
        return chunks

    def _parallel_for_sum(self, numbers, num_workers):
        """Sumowanie z użyciem ProcessPoolExecutor (odpowiednik Parallel.For)."""
        chunks = self._split_into_chunks(numbers, num_workers)
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            partial_sums = list(executor.map(_sum_chunk, chunks))
        return sum(partial_sums)

    def run(self):
        """Uruchamia porównanie: sekwencyjne vs Parallel.For (4 i 8 workerów)."""
        self._load_data()
        numbers = self.numbers

        print("\n" + "-" * 60)
        print("  Parallel.For (ProcessPoolExecutor) — sumowanie tablicy")
        print("-" * 60)

        # Sekwencyjnie
        start = time.perf_counter()
        seq_sum = self._sequential_sum(numbers)
        seq_time = (time.perf_counter() - start) * 1000

        # 4 workery
        start = time.perf_counter()
        p4_sum = self._parallel_for_sum(numbers, 4)
        p4_time = (time.perf_counter() - start) * 1000

        # 8 workerów
        start = time.perf_counter()
        p8_sum = self._parallel_for_sum(numbers, 8)
        p8_time = (time.perf_counter() - start) * 1000

        print(f"  Metoda sekwencyjna              – suma: {seq_sum}, czas wykonania: {seq_time:.4f} ms")
        print(f"  Parallel.For (4 workery)        – suma: {p4_sum}, czas wykonania: {p4_time:.4f} ms")
        print(f"  Parallel.For (8 workerów)       – suma: {p8_sum}, czas wykonania: {p8_time:.4f} ms")

        return {
            'sekwencyjna': {'suma': seq_sum, 'czas_ms': seq_time},
            'parallel_for_4': {'suma': p4_sum, 'czas_ms': p4_time},
            'parallel_for_8': {'suma': p8_sum, 'czas_ms': p8_time},
        }
