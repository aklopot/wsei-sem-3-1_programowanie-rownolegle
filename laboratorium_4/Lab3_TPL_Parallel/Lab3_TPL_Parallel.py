"""
Laboratorium 4 - Zadanie 3: TPL / Parallel (concurrent.futures)
Odpowiednik C# Task Parallel Library w Pythonie:
  1) Parallel.For — sumowanie tablicy (ProcessPoolExecutor)
  2) Parallel.ForEach — przetwarzanie wielu plików CSV równolegle
  3) Pełny benchmark metod z zadań 1-3 + zapis logu
"""

from src.modules.parallel_for_calculator import ParallelForCalculator
from src.modules.parallel_foreach_calculator import ParallelForEachCalculator
from src.modules.benchmark_runner import BenchmarkRunner
from src.utils.menu import Menu


def main():
    """Funkcja główna — tworzy menu i uruchamia wybraną opcję."""
    menu = Menu(title="LAB 4 - ZADANIE 3: TPL / PARALLEL")

    pfor_calc = ParallelForCalculator()
    pforeach_calc = ParallelForEachCalculator()
    benchmark = BenchmarkRunner()

    menu.add_option(
        '1',
        'Parallel.For — sumowanie tablicy (4/8 workerów)',
        lambda: pfor_calc.run(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Parallel.ForEach — przetwarzanie 4 plików CSV równolegle',
        lambda: pforeach_calc.run(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Pełny benchmark (zadania 1-3) + zapis logu',
        lambda: benchmark.run(),
        display_order=3
    )
    menu.add_option(
        '0',
        'Wyjście',
        lambda: menu.exit(),
        display_order=99
    )
    menu.show()


if __name__ == "__main__":
    main()
