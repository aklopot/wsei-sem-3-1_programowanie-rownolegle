"""
Kalkulator sumy z użyciem threading.Thread.
Porównanie sumowania sekwencyjnego z wielowątkowym.
Uwaga: z powodu GIL w CPythonie, threading.Thread nie daje przyspieszenia dla zadań CPU-bound.
"""

import os
import threading
import time

from src.modules.csv_loader import load_numbers_from_csv


class ThreadSumCalculator:
    """
    Oblicza sumę liczb metodami:
    - sekwencyjną
    - threading.Thread z 2 i 8 wątkami
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
    def _partial_sum(numbers, start, end, results, index):
        """Oblicza sumę częściową dla fragmentu tablicy (używane przez wątki)."""
        partial = 0
        for i in range(start, end):
            partial += numbers[i]
        results[index] = partial

    def _threaded_sum(self, numbers, num_threads):
        """Oblicza sumę z użyciem threading.Thread dla podanej liczby wątków."""
        n = len(numbers)
        chunk_size = n // num_threads
        threads = []
        results = [0] * num_threads

        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size if i < num_threads - 1 else n
            t = threading.Thread(
                target=self._partial_sum,
                args=(numbers, start, end, results, i)
            )
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        return sum(results)

    def run(self):
        """Uruchamia porównanie: sekwencyjne vs threading.Thread (2, 8 wątków)."""
        self._load_data()
        numbers = self.numbers

        print("\n" + "-"*60)
        print("  Wersja 1: threading.Thread (GIL - brak zysku)")
        print("-"*60)

        # Sekwencyjnie
        start = time.perf_counter()
        seq_sum = self._sequential_sum(numbers)
        seq_time = (time.perf_counter() - start) * 1000

        # 2 wątki
        start = time.perf_counter()
        t2_sum = self._threaded_sum(numbers, 2)
        t2_time = (time.perf_counter() - start) * 1000

        # 8 wątków
        start = time.perf_counter()
        t8_sum = self._threaded_sum(numbers, 8)
        t8_time = (time.perf_counter() - start) * 1000

        print(f"  Metoda sekwencyjna            – suma: {seq_sum}, czas wykonania: {seq_time:.4f} ms")
        print(f"  Metoda wielowątkowa (2 wątki)  – suma: {t2_sum}, czas wykonania: {t2_time:.4f} ms")
        print(f"  Metoda wielowątkowa (8 wątków) – suma: {t8_sum}, czas wykonania: {t8_time:.4f} ms")

        print("\n  [INFO] threading.Thread podlega GIL — brak realnej równoległości dla zadań CPU-bound.")
