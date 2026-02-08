"""
Odpowiednik Parallel.ForEach() z TPL (C#).
W Pythonie realizowany przez concurrent.futures.ProcessPoolExecutor.

Przetwarza wiele plików CSV równolegle — każdy plik w oddzielnym procesie.
Pliki: numbers1.csv, numbers2.csv, numbers3.csv, numbers4.csv.
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor

from src.modules.csv_loader import load_numbers_from_csv

DATA_DIR = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'dane_wejsciowe'
)

CSV_FILES = [
    'numbers1.csv',
    'numbers2.csv',
    'numbers3.csv',
    'numbers4.csv',
]


def _process_single_file(filepath):
    """
    Funkcja robocza — wczytuje plik CSV i oblicza sumę.
    Musi być na poziomie modułu (wymagane przez ProcessPoolExecutor).
    """
    abs_path = os.path.abspath(filepath)
    with open(abs_path, 'r') as f:
        content = f.read().strip()
    numbers = [int(x) for x in content.split(';') if x.strip()]
    total = 0
    for num in numbers:
        total += num
    return {
        'file': os.path.basename(filepath),
        'count': len(numbers),
        'sum': total,
    }


class ParallelForEachCalculator:
    """
    Przetwarzanie wielu plików CSV z użyciem Parallel.ForEach (ProcessPoolExecutor).
    Porównanie: sekwencyjne vs równoległe przetwarzanie 4 plików.
    """

    def __init__(self):
        self.file_paths = [os.path.join(DATA_DIR, f) for f in CSV_FILES]

    def _sequential_foreach(self):
        """Przetwarza pliki sekwencyjnie, jeden po drugim."""
        results = []
        for fp in self.file_paths:
            results.append(_process_single_file(fp))
        return results

    def _parallel_foreach(self):
        """Przetwarza pliki równolegle z ProcessPoolExecutor (Parallel.ForEach)."""
        with ProcessPoolExecutor(max_workers=len(self.file_paths)) as executor:
            results = list(executor.map(_process_single_file, self.file_paths))
        return results

    def run(self):
        """Uruchamia porównanie: sekwencyjne vs Parallel.ForEach na 4 plikach CSV."""
        print("\n" + "-" * 60)
        print("  Parallel.ForEach (ProcessPoolExecutor) — przetwarzanie plików")
        print(f"  Pliki: {', '.join(CSV_FILES)}")
        print("-" * 60)

        # Sekwencyjnie
        start = time.perf_counter()
        seq_results = self._sequential_foreach()
        seq_time = (time.perf_counter() - start) * 1000

        # Równolegle
        start = time.perf_counter()
        par_results = self._parallel_foreach()
        par_time = (time.perf_counter() - start) * 1000

        print(f"\n  Wyniki sekwencyjne:")
        for r in seq_results:
            print(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}")
        print(f"  Czas: {seq_time:.4f} ms")

        print(f"\n  Wyniki Parallel.ForEach:")
        for r in par_results:
            print(f"    {r['file']}: {r['count']} liczb, suma = {r['sum']}")
        print(f"  Czas: {par_time:.4f} ms")

        total_seq = sum(r['sum'] for r in seq_results)
        total_par = sum(r['sum'] for r in par_results)
        print(f"\n  Suma globalna (sekw.):  {total_seq}")
        print(f"  Suma globalna (równ.):  {total_par}")
        print(f"  Zgodność: {'TAK' if total_seq == total_par else 'NIE'}")

        return {
            'sekwencyjna': {'wyniki': seq_results, 'czas_ms': seq_time},
            'parallel_foreach': {'wyniki': par_results, 'czas_ms': par_time},
        }
