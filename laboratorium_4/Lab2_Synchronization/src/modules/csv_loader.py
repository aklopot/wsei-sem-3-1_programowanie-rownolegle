"""
Moduł ładowania danych CSV.
Wczytuje tablicę liczb całkowitych z plików CSV (separator: średnik).
"""

import os


def load_numbers_from_csv(filepath):
    """
    Wczytuje liczby całkowite z pliku CSV rozdzielone średnikiem.

    Args:
        filepath (str): Ścieżka do pliku CSV.

    Returns:
        list[int]: Lista liczb całkowitych wczytanych z pliku.
    """
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Nie znaleziono pliku: {abs_path}")

    with open(abs_path, 'r') as f:
        content = f.read().strip()

    numbers = [int(x) for x in content.split(';') if x.strip()]
    return numbers
