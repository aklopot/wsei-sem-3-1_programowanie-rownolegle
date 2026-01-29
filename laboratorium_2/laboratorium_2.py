"""
Laboratorium 2: Zadania
"""

# from src.modules.fibonacci_calculator import FibonacciCalculator
from src.modules.integral_calculator import IntegralCalculator
from src.utils.menu import Menu


def main_laboratorium_2():
    """Funkcja główna - tworzy menu i dodaje opcje."""
    menu = Menu(title="LABORATORIUM 2 - ZADANIA")
    
    menu.add_option(
        '1',
        'Oblicz całkę numeryczną dla wybranej funkcji metodą trapezów (jednowątkowo)',
        lambda: IntegralCalculator().run_task1(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Oblicz całkę dla trzech przedziałów równolegle (threading.Thread)',
        lambda: IntegralCalculator().run_task2(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Oblicz całkę - wybór metody (Thread vs Executor)',
        lambda: IntegralCalculator().run_task3(),
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
    main_laboratorium_2()

