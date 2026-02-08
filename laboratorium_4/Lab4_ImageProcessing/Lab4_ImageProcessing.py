"""
Laboratorium 4 - Zadanie 4: Przetwarzanie obrazów
Równoległe przetwarzanie obrazów (filtr szarości piksel po pikselu).
  1) Sekwencyjne — obraz po obrazie
  2) Równoległe — każdy obraz w osobnym procesie (ProcessPoolExecutor)
  3) Porównanie obu metod + zapis logu
"""

from src.modules.image_processor import ImageProcessor
from src.utils.menu import Menu


def main():
    """Funkcja główna — tworzy menu i uruchamia wybraną opcję."""
    menu = Menu(title="LAB 4 - ZADANIE 4: PRZETWARZANIE OBRAZÓW")

    processor = ImageProcessor()

    menu.add_option(
        '1',
        'Przetwarzanie sekwencyjne (filtr szarości)',
        lambda: processor.run_sequential(),
        display_order=1
    )
    menu.add_option(
        '2',
        'Przetwarzanie równoległe (filtr szarości)',
        lambda: processor.run_parallel(),
        display_order=2
    )
    menu.add_option(
        '3',
        'Porównanie sekwencyjne vs równoległe + log',
        lambda: processor.run_comparison(),
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
