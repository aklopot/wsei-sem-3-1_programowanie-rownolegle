"""
Przetwarzanie obrazów — filtr szarości (grayscale).
Konwersja piksel po pikselu: gray = 0.299*R + 0.587*G + 0.114*B.

Porównanie:
  - sekwencyjne przetwarzanie (obraz po obrazie)
  - równoległe przetwarzanie (multiprocessing — każdy obraz w osobnym procesie)

Logger zapisuje postępy i czasy do pliku tekstowego.
"""

import os
import time
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

from src.modules.image_loader import load_image_paths

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'wyniki')
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..')


def _apply_grayscale(input_path, output_path):
    """
    Konwertuje obraz na szarość piksel po pikselu.
    Celowo wolna metoda (pure Python) — widoczny zysk z równoległości.
    Zwraca dict z informacjami o przetworzonym obrazie.
    """
    img = Image.open(input_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            pixels[x, y] = (gray, gray, gray)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

    return {
        'file': os.path.basename(input_path),
        'size': f'{width}x{height}',
        'output': os.path.basename(output_path),
    }


def _worker_grayscale(args):
    """
    Funkcja robocza dla ProcessPoolExecutor.
    Przyjmuje tuple (input_path, output_path).
    """
    input_path, output_path = args
    start = time.perf_counter()
    result = _apply_grayscale(input_path, output_path)
    result['czas_ms'] = (time.perf_counter() - start) * 1000
    return result


class ImageProcessor:
    """
    Przetwarzanie obrazów: filtr szarości.
    Sekwencyjnie i równolegle (ProcessPoolExecutor).
    """

    def __init__(self):
        self.image_paths = None

    def _load_images(self):
        """Wczytuje ścieżki do obrazów z folderu wejściowego."""
        if self.image_paths is None:
            self.image_paths = load_image_paths()
            if not self.image_paths:
                return False
        return True

    def _build_output_path(self, input_path, prefix):
        """Tworzy ścieżkę wyjściową z prefiksem."""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        return os.path.join(OUTPUT_DIR, f'{prefix}_{name}{ext}')

    def run_sequential(self):
        """Przetwarzanie sekwencyjne — obraz po obrazie."""
        if not self._load_images():
            return None, 0

        print("\n" + "-" * 60)
        print("  Przetwarzanie SEKWENCYJNE — filtr szarości")
        print("-" * 60)

        tasks = [(p, self._build_output_path(p, 'seq')) for p in self.image_paths]

        start_time = time.perf_counter()
        results = []
        for input_path, output_path in tasks:
            print(f"  Przetwarzam: {os.path.basename(input_path)}...")
            r = _worker_grayscale((input_path, output_path))
            results.append(r)
            print(f"    → {r['output']} ({r['size']}) — {r['czas_ms']:.2f} ms")

        total_time = (time.perf_counter() - start_time) * 1000

        print(f"\n  Łączny czas sekwencyjny: {total_time:.2f} ms")
        print(f"  Wyniki w folderze: wyniki/")
        return results, total_time

    def run_parallel(self):
        """Przetwarzanie równoległe — każdy obraz w osobnym procesie."""
        if not self._load_images():
            return None, 0

        print("\n" + "-" * 60)
        print("  Przetwarzanie RÓWNOLEGŁE — filtr szarości")
        print(f"  (ProcessPoolExecutor, {len(self.image_paths)} workerów)")
        print("-" * 60)

        tasks = [(p, self._build_output_path(p, 'par')) for p in self.image_paths]
        num_workers = len(tasks)

        print(f"  Uruchamiam {num_workers} procesów równolegle...")

        start_time = time.perf_counter()
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(_worker_grayscale, tasks))
        total_time = (time.perf_counter() - start_time) * 1000

        for r in results:
            print(f"    {r['file']} → {r['output']} ({r['size']}) — {r['czas_ms']:.2f} ms")

        print(f"\n  Łączny czas równoległy: {total_time:.2f} ms")
        print(f"  Wyniki w folderze: wyniki/")
        return results, total_time

    def run_comparison(self):
        """Porównanie obu metod + zapis logu."""
        if not self._load_images():
            return
        log_path = os.path.join(LOG_DIR, 'processing_log.txt')

        print("\n" + "=" * 60)
        print("  PORÓWNANIE: SEKWENCYJNE vs RÓWNOLEGŁE")
        print("=" * 60)

        seq_results, seq_time = self.run_sequential()
        par_results, par_time = self.run_parallel()

        print("\n" + "=" * 60)
        print("  PODSUMOWANIE")
        print("=" * 60)
        print(f"  Czas sekwencyjny:  {seq_time:.2f} ms")
        print(f"  Czas równoległy:   {par_time:.2f} ms")
        if par_time > 0:
            speedup = seq_time / par_time
            print(f"  Przyspieszenie:    {speedup:.2f}x")

        # Zapis logu
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("=" * 60 + "\n")
            log.write("  LOG PRZETWARZANIA OBRAZÓW — FILTR SZAROŚCI\n")
            log.write("=" * 60 + "\n\n")

            log.write("--- Przetwarzanie sekwencyjne ---\n\n")
            for r in seq_results:
                log.write(f"  {r['file']} ({r['size']}) → {r['output']} — {r['czas_ms']:.2f} ms\n")
            log.write(f"\n  Łączny czas: {seq_time:.2f} ms\n")

            log.write(f"\n--- Przetwarzanie równoległe ---\n\n")
            for r in par_results:
                log.write(f"  {r['file']} ({r['size']}) → {r['output']} — {r['czas_ms']:.2f} ms\n")
            log.write(f"\n  Łączny czas: {par_time:.2f} ms\n")

            log.write(f"\n{'='*60}\n")
            log.write(f"PODSUMOWANIE\n")
            log.write(f"  Sekwencyjnie: {seq_time:.2f} ms\n")
            log.write(f"  Równolegle:   {par_time:.2f} ms\n")
            if par_time > 0:
                log.write(f"  Przyspieszenie: {seq_time / par_time:.2f}x\n")
            log.write("=" * 60 + "\n")

        print(f"\n  Log zapisany do: processing_log.txt")
