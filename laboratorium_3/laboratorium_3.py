"""
Laboratorium 3: Zadania
Rozbudowa aplikacji o różne metody przetwarzania równoległego:
- Thread (threading.Thread)
- ThreadPool (multiprocessing.pool.ThreadPool)
- TPL (concurrent.futures.ThreadPoolExecutor)
- BackgroundWorker (symulacja z threading)
"""

from src.modules.integral_calculator import IntegralCalculator
from src.utils.menu import Menu


def main_laboratorium_3():
    """Main function - creates menu and adds options."""
    menu = Menu(title="LABORATORIUM 3 - ZADANIA")
    
    calculator = IntegralCalculator()
    
    menu.add_option(
        '1',
        'Oblicz całkę (Thread - threading.Thread)',
        lambda: calculator.run_thread_calculation(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Oblicz całkę (ThreadPool - multiprocessing.pool.ThreadPool)',
        lambda: calculator.run_threadpool_calculation(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Oblicz całkę (TPL - ThreadPoolExecutor)',
        lambda: calculator.run_tpl_calculation(),
        display_order=3
    )
    menu.add_option(
        '4',
        'Oblicz całkę (BackgroundWorker)',
        lambda: calculator.run_backgroundworker_calculation(),
        display_order=4
    )
    menu.add_option(
        '5',
        'Porównanie wszystkich metod (benchmark)',
        lambda: calculator.run_benchmark(),
        display_order=5
    )
    menu.add_option(
        '0',
        'Wyjście',
        lambda: menu.exit(),
        display_order=99
    )
    menu.show()


if __name__ == "__main__":
    main_laboratorium_3()
