"""
Kalkulator sumy z użyciem multiprocessing.Process — wersja z synchronizacją i bez.
Każdy proces zapisuje wyniki cząstkowe (sumę, średnią) do wspólnej listy (Manager).
Logger zapisuje postępy do wspólnego pliku tekstowego.
Przetwarzanie dla 4 procesów.

multiprocessing omija GIL — race condition jest bardziej widoczny niż w threading.
"""

import os
import time
import multiprocessing

from src.modules.csv_loader import load_numbers_from_csv

NUM_PROCESSES = 4
LOG_INTERVAL = 500


# ---- Funkcje robocze procesów (muszą być na poziomie modułu) ----

def _process_worker_sync(proc_id, numbers, start, end,
                         shared_results, results_lock,
                         shared_counter, counter_lock,
                         log_path, file_lock):
    """Funkcja procesu z synchronizacją (Lock)."""
    partial_sum = 0
    for i in range(start, end):
        partial_sum += numbers[i]
        position = i - start + 1
        average = partial_sum / position

        with results_lock:
            shared_results.append({
                'proc_id': proc_id,
                'position': position,
                'partial_sum': partial_sum,
                'average': round(average, 2)
            })

        with counter_lock:
            shared_counter['total_sum'] += numbers[i]
            shared_counter['count'] += 1

        if position % LOG_INTERVAL == 0 or position == (end - start):
            with file_lock:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(
                        f"Proces {proc_id}: poz={position:>5}, "
                        f"suma_cząstkowa={partial_sum:>10}, "
                        f"średnia={average:>10.2f}\n"
                    )


def _process_worker_unsync(proc_id, numbers, start, end,
                           shared_results, shared_counter,
                           log_path):
    """
    Funkcja procesu BEZ synchronizacji.
    Operacja read-modify-write na shared_counter (Manager.dict)
    jest nie-atomowa — między odczytem a zapisem inny proces
    może zmienić wartość (race condition).
    """
    partial_sum = 0
    for i in range(start, end):
        partial_sum += numbers[i]
        position = i - start + 1
        average = partial_sum / position

        shared_results.append({
            'proc_id': proc_id,
            'position': position,
            'partial_sum': partial_sum,
            'average': round(average, 2)
        })

        # Celowo nie-atomowa operacja read-modify-write
        # Każda operacja na Manager.dict to osobne wywołanie IPC,
        # więc inne procesy mogą się wcisnąć między odczyt a zapis
        current_sum = shared_counter['total_sum']
        current_count = shared_counter['count']
        shared_counter['total_sum'] = current_sum + numbers[i]
        shared_counter['count'] = current_count + 1

        if position % LOG_INTERVAL == 0 or position == (end - start):
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(
                    f"Proces {proc_id}: poz={position:>5}, "
                    f"suma_cząstkowa={partial_sum:>10}, "
                    f"średnia={average:>10.2f}\n"
                )


class ProcessSyncCalculator:
    """
    Sumowanie z użyciem multiprocessing.Process (4 procesy).
    Dwie wersje: z Lock (poprawna) i bez Lock (race condition).
    Używa Manager() do współdzielenia listy i słownika między procesami.
    """

    DATA_FILE = os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'dane_wejsciowe', 'numbers1.csv'
    )
    LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..')

    def __init__(self):
        self.numbers = None

    def _load_data(self):
        """Wczytuje dane z CSV, jeśli jeszcze nie wczytano."""
        if self.numbers is None:
            self.numbers = load_numbers_from_csv(self.DATA_FILE)
            print(f"  Wczytano {len(self.numbers)} liczb z pliku CSV.")

    def _run(self, use_lock):
        """Wspólna logika dla obu wersji."""
        self._load_data()
        numbers = self.numbers
        n = len(numbers)
        chunk_size = n // NUM_PROCESSES

        manager = multiprocessing.Manager()
        shared_results = manager.list()
        shared_counter = manager.dict({'total_sum': 0, 'count': 0})

        mode = "Z_LOCK" if use_lock else "BEZ_LOCK"
        log_name = f'log_process_{mode.lower()}.txt'
        log_path = os.path.abspath(os.path.join(self.LOG_DIR, log_name))

        print("\n" + "-" * 60)
        if use_lock:
            print(f"  multiprocessing.Process — Z synchronizacją (Lock) — {NUM_PROCESSES} procesy")
        else:
            print(f"  multiprocessing.Process — BEZ synchronizacji — {NUM_PROCESSES} procesy")
            print("  [UWAGA] Brak Lock — możliwy wyścig procesów (race condition)!")
        print("-" * 60)

        results_lock = multiprocessing.Lock()
        counter_lock = multiprocessing.Lock()
        file_lock = multiprocessing.Lock()

        # Nagłówek logu
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== LOG: multiprocessing.Process — {mode} ===\n")
            f.write(f"Procesów: {NUM_PROCESSES}, elementów: {n}\n\n")

        processes = []
        start_time = time.perf_counter()

        for p_id in range(NUM_PROCESSES):
            s = p_id * chunk_size
            e = s + chunk_size if p_id < NUM_PROCESSES - 1 else n

            if use_lock:
                p = multiprocessing.Process(
                    target=_process_worker_sync,
                    args=(p_id + 1, numbers, s, e,
                          shared_results, results_lock,
                          shared_counter, counter_lock,
                          log_path, file_lock)
                )
            else:
                p = multiprocessing.Process(
                    target=_process_worker_unsync,
                    args=(p_id + 1, numbers, s, e,
                          shared_results, shared_counter,
                          log_path)
                )
            processes.append(p)

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        elapsed = (time.perf_counter() - start_time) * 1000
        expected = sum(numbers)

        # Podsumowanie do pliku
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"PODSUMOWANIE\n{'='*50}\n")
            f.write(f"  Suma ze shared_counter: {shared_counter['total_sum']}\n")
            f.write(f"  Licznik:                {shared_counter['count']} (oczekiwano: {n})\n")
            f.write(f"  Suma oczekiwana:        {expected}\n")

        # Wyniki cząstkowe procesów
        results_list = list(shared_results)
        proc_final = {}
        for entry in results_list:
            proc_final[entry['proc_id']] = entry

        print(f"\n  Wyniki cząstkowe procesów:")
        for pid in sorted(proc_final.keys()):
            e = proc_final[pid]
            print(f"    Proces {pid}: suma = {e['partial_sum']:>10}, "
                  f"średnia = {e['average']:>10.2f}")

        actual = shared_counter['total_sum']
        actual_count = shared_counter['count']

        print(f"\n  Wpisów we wspólnej liście: {len(results_list)}")
        print(f"  Suma (shared_counter):  {actual}")
        print(f"  Licznik elementów:      {actual_count} (oczekiwano: {n})")
        print(f"  Suma oczekiwana:        {expected}")

        if actual != expected:
            lost = expected - actual
            print(f"\n  BŁĄD WYŚCIGU: utracono {lost} ({lost/expected*100:.1f}% sumy)")
        else:
            print(f"\n  Zgodność: TAK")

        print(f"  Czas wykonania: {elapsed:.2f} ms")
        print(f"  Log: {log_name}")

    def run_synchronized(self):
        """Wersja Z synchronizacją."""
        self._run(use_lock=True)

    def run_unsynchronized(self):
        """Wersja BEZ synchronizacji."""
        self._run(use_lock=False)
