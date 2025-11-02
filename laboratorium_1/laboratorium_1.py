"""
Laboratorium 1: Zadania
Program wykonuje różne obliczenia, w tym ciąg Fibonacciego i całki numeryczne.
Dostępne opcje:
1. Oblicz pierwsze n elementów ciągu Fibonacciego
2. Oblicz fragment ciągu Fibonacciego od indeksu L1 przez L2 elementów
3. Oblicz całkę numeryczną metodą prostokątów
"""

from src.modules.fibonacci_calculator import FibonacciCalculator
from src.modules.integral_calculator import IntegralCalculator
from src.utils.menu import Menu


def main_laboratorium_1():
    """Funkcja główna - tworzy menu i dodaje opcje."""
    menu = Menu(title="LABORATORIUM 1 - ZADANIA")
    
    # Dodaj opcje do menu
    menu.add_option(
        '1',
        'Oblicz pierwsze n elementów ciągu Fibonacciego',
        lambda: FibonacciCalculator().run_task1(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Oblicz fragment ciągu Fibonacciego od indeksu (L1) przez L2 elementów',
        lambda: FibonacciCalculator().run_task2(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Oblicz całkę numeryczną f(x) = 1/2 * x metodą prostokątów',
        lambda: IntegralCalculator().run_task3(),
        display_order=3
    )
    menu.add_option(
        '4',
        'Analiza wpływu liczby elementów na dokładność całki (n=3,7,13)',
        lambda: IntegralCalculator().run_task4(),
        display_order=4
    )
    menu.add_option(
        '5',
        'Porównanie metod obliczania całki (lewa, środek, prawa)',
        lambda: IntegralCalculator().run_task5(),
        display_order=5
    )
    menu.add_option(
        '6',
        'Porównanie prostokątów i trapezów',
        lambda: IntegralCalculator().run_task6(),
        display_order=6
    )
    menu.add_option(
        '0',
        'Wyjście',
        lambda: menu.exit(),
        display_order=99
    )
    menu.show()


if __name__ == "__main__":
    main_laboratorium_1()

