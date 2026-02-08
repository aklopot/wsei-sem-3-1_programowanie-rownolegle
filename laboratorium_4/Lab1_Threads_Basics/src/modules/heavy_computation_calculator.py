"""
Kalkulator ciężkich obliczeń z użyciem multiprocessing.Pool.
Demonstruje, że równoległość opłaca się gdy praca na element jest wystarczająco duża.

Każdy element przechodzi 10000 iteracji sin/cos, co daje ~6s pracy sekwencyjnej.
Dzięki temu multiprocessing.Pool ma wystarczająco dużo pracy, aby pokonać narzut
tworzenia procesów na Windows i pokazać realne przyspieszenie.
"""

import math
import os
import time
from multiprocessing import Pool

from src.modules.csv_loader import load_numbers_from_csv

ITERATIONS_PER_ELEMENT = 10000


def _heavy_worker(chunk):
    """
    Funkcja robocza procesu: dla każdej liczby wykonuje N iteracji
    wzoru sin*cos+1, a następnie sumuje wyniki.
    Symuluje zadanie intensywne obliczeniowo.
    """
    total = 0.0
    for num in chunk:
        val = float(num)
        for _ in range(ITERATIONS_PER_ELEMENT):
            val = math.sin(val) * math.cos(val) + 1.0
        total += val
    return total


class HeavyComputationCalculator:
    """
    Porównuje metodę sekwencyjną z multiprocessing.Pool (2, 8 procesów)
    na zadaniu intensywnym obliczeniowo (ciężkie obliczenie na każdy element).
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
    def _sequential_heavy(numbers):
        """Ciężkie obliczenie wykonane sekwencyjnie."""
        total = 0.0
        for num in numbers:
            val = float(num)
            for _ in range(ITERATIONS_PER_ELEMENT):
                val = math.sin(val) * math.cos(val) + 1.0
            total += val
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

    def _multiprocess_heavy(self, numbers, num_processes):
        """Ciężkie obliczenie z użyciem multiprocessing.Pool."""
        chunks = self._split_into_chunks(numbers, num_processes)
        with Pool(processes=num_processes) as pool:
            partial_results = pool.map(_heavy_worker, chunks)
        return sum(partial_results)

    def run(self):
        """Uruchamia porównanie: sekwencyjne vs multiprocessing z ciężkim obliczeniem."""
        self._load_data()
        numbers = self.numbers

        print("\n" + "-" * 60)
        print(f"  Wersja 3: Ciężkie obliczenia + multiprocessing.Pool")
        print("-" * 60)
        print(f"  Obliczenie: każda z {len(numbers)} liczb jest wartością startową val.")
        print(f"  Dla każdej liczby powtarzamy {ITERATIONS_PER_ELEMENT}x: val = sin(val)*cos(val)+1.0")
        print(f"  (wynik jednej iteracji staje się wejściem następnej).")
        print(f"  Końcowe val z każdego elementu sumujemy w wynik globalny.")
        print()
        print("  Obliczam sekwencyjnie... (to potrwa kilka sekund)")

        # Sekwencyjnie
        start = time.perf_counter()
        seq_result = self._sequential_heavy(numbers)
        seq_time = (time.perf_counter() - start) * 1000

        # 2 procesy
        print("  Obliczam równolegle (2 procesy)...")
        start = time.perf_counter()
        p2_result = self._multiprocess_heavy(numbers, 2)
        p2_time = (time.perf_counter() - start) * 1000

        # 8 procesów
        print("  Obliczam równolegle (8 procesów)...")
        start = time.perf_counter()
        p8_result = self._multiprocess_heavy(numbers, 8)
        p8_time = (time.perf_counter() - start) * 1000

        print()
        print(f"  Metoda sekwencyjna              – wynik: {seq_result:.2f}, czas wykonania: {seq_time:.2f} ms")
        print(f"  Metoda wieloprocesowa (2 proc.) – wynik: {p2_result:.2f}, czas wykonania: {p2_time:.2f} ms")
        print(f"  Metoda wieloprocesowa (8 proc.) – wynik: {p8_result:.2f}, czas wykonania: {p8_time:.2f} ms")

        print()
        if seq_time > 0:
            speedup_2 = seq_time / p2_time
            speedup_8 = seq_time / p8_time
            print(f"  Przyspieszenie (2 proc.): {speedup_2:.2f}x")
            print(f"  Przyspieszenie (8 proc.): {speedup_8:.2f}x")

        print(f"\n  [INFO] Przy wystarczająco ciężkim obliczeniu na element, multiprocessing.Pool")
        print(f"         pokazuje realny zysk — narzut tworzenia procesów jest pomijalny")
        print(f"         w porównaniu do {seq_time / 1000:.1f}s pracy obliczeniowej.")
