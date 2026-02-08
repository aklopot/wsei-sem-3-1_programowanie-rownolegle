"""
Moduł ładowania obrazów z folderu wejściowego.
Oczekuje min. 4 obrazów w dane_wejsciowe/images/.
"""

import os

IMAGES_DIR = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'dane_wejsciowe', 'images'
)

SUPPORTED_EXT = ('.png', '.jpg', '.jpeg', '.bmp')


def load_image_paths():
    """
    Zwraca listę ścieżek do obrazów z folderu wejściowego.
    Jeśli brak obrazów — wypisuje komunikat i zwraca pustą listę.
    """
    if not os.path.isdir(IMAGES_DIR):
        print(f"\n  BŁĄD: Nie znaleziono folderu z obrazami:")
        print(f"    {os.path.abspath(IMAGES_DIR)}")
        print(f"\n  Utwórz folder dane_wejsciowe/images/ i umieść w nim min. 4 obrazy kolorowe.")
        return []

    image_files = sorted([
        f for f in os.listdir(IMAGES_DIR)
        if f.lower().endswith(SUPPORTED_EXT)
    ])

    if len(image_files) == 0:
        print(f"\n  BŁĄD: Folder dane_wejsciowe/images/ jest pusty.")
        print(f"  Umieść w nim min. 4 obrazy kolorowe ({', '.join(SUPPORTED_EXT)}).")
        return []

    if len(image_files) < 4:
        print(f"\n  UWAGA: Znaleziono tylko {len(image_files)} obrazów (wymagane min. 4).")
        print(f"  Dodaj więcej obrazów do dane_wejsciowe/images/.")
        return []

    paths = [os.path.join(IMAGES_DIR, f) for f in image_files]
    print(f"  Znaleziono {len(image_files)} obrazów w folderze wejściowym.")
    return paths
