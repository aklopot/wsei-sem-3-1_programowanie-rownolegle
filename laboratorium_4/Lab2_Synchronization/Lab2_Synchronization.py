"""
Laboratorium 4 - Zadanie 2: Synchronizacja wątków/procesów
Rozszerzenie zadania 1 o:
  - wspólną listę wyników cząstkowych (suma, średnia)
  - synchronizację dostępu (Lock) i wersję bez synchronizacji (race condition)
  - Logger zapisujący postępy do pliku
Przetwarzanie dla 4 wątków/procesów.
"""

from src.modules.thread_sync_calculator import ThreadSyncCalculator
from src.modules.process_sync_calculator import ProcessSyncCalculator
from src.utils.menu import Menu


def main():
    """Funkcja główna — tworzy menu i uruchamia wybraną opcję."""
    menu = Menu(title="LAB 4 - ZADANIE 2: SYNCHRONIZACJA")

    thread_calc = ThreadSyncCalculator()
    process_calc = ProcessSyncCalculator()

    menu.add_option(
        '1',
        'threading.Thread (4 wątki) — Z synchronizacją (Lock)',
        lambda: thread_calc.run_synchronized(),
        display_order=1
    )
    menu.add_option(
        '2',
        'threading.Thread (4 wątki) — BEZ synchronizacji (race condition)',
        lambda: thread_calc.run_unsynchronized(),
        display_order=2
    )
    menu.add_option(
        '3',
        'multiprocessing.Process (4 procesy) — Z synchronizacją (Lock)',
        lambda: process_calc.run_synchronized(),
        display_order=3
    )
    menu.add_option(
        '4',
        'multiprocessing.Process (4 procesy) — BEZ synchronizacji (race condition)',
        lambda: process_calc.run_unsynchronized(),
        display_order=4
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
