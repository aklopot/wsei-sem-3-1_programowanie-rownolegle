"""
Laboratorium 4 - Zadanie 1: Sumowanie tablicy liczb
Porównanie metod:
  1) threading.Thread (2 i 8 wątków) — ograniczone przez GIL
  2) multiprocessing.Pool (2 i 8 procesów) — prawdziwa równoległość
  3) Ciężkie obliczenia + multiprocessing.Pool — demonstracja realnego zysku
"""

from src.modules.thread_sum_calculator import ThreadSumCalculator
from src.modules.multiprocess_sum_calculator import MultiprocessSumCalculator
from src.modules.heavy_computation_calculator import HeavyComputationCalculator
from src.utils.menu import Menu


def main():
    """Funkcja główna — tworzy menu i uruchamia wybraną opcję."""
    menu = Menu(title="LAB 4 - ZADANIE 1: SUMOWANIE TABLICY LICZB")

    thread_calc = ThreadSumCalculator()
    mp_calc = MultiprocessSumCalculator()
    heavy_calc = HeavyComputationCalculator()

    menu.add_option(
        '1',
        'Sumowanie: sekwencyjne + threading.Thread (2/8 wątków)',
        lambda: thread_calc.run(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Sumowanie: sekwencyjne + multiprocessing.Pool (2/8 procesów)',
        lambda: mp_calc.run(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Demo: 10000x sin/cos na element + multiprocessing.Pool (2/8 proc.)',
        lambda: heavy_calc.run(),
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
