"""
Kalkulator sumy z użyciem threading.Thread — wersja z synchronizacją i bez.
Każdy wątek zapisuje wyniki cząstkowe (sumę, średnią) do wspólnej listy.
Logger zapisuje postępy do wspólnego pliku tekstowego.
Przetwarzanie dla 4 wątków.
"""

import os
import threading
import time

from src.modules.csv_loader import load_numbers_from_csv

NUM_THREADS = 4
LOG_INTERVAL = 500


class ThreadSyncCalculator:
    """
    Sumowanie z użyciem threading.Thread (4 wątki).
    Dwie wersje: z Lock (poprawna) i bez Lock (race condition).
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

    # -----------------------------------------------------------------
    #  Funkcje robocze wątków
    # -----------------------------------------------------------------

    @staticmethod
    def _worker_sync(thread_id, numbers, start, end,
                     shared_results, results_lock,
                     shared_counter, counter_lock,
                     log_file, file_lock):
        """Funkcja wątku Z synchronizacją (Lock)."""
        partial_sum = 0
        for i in range(start, end):
            partial_sum += numbers[i]
            position = i - start + 1
            average = partial_sum / position

            with results_lock:
                shared_results.append({
                    'thread_id': thread_id,
                    'position': position,
                    'partial_sum': partial_sum,
                    'average': round(average, 2)
                })

            with counter_lock:
                shared_counter['total_sum'] += numbers[i]
                shared_counter['count'] += 1

            if position % LOG_INTERVAL == 0 or position == (end - start):
                with file_lock:
                    log_file.write(
                        f"Wątek {thread_id}: poz={position:>5}, "
                        f"suma_cząstkowa={partial_sum:>10}, "
                        f"średnia={average:>10.2f}\n"
                    )

    @staticmethod
    def _worker_unsync(thread_id, numbers, start, end,
                       shared_results, shared_counter,
                       log_file):
        """
        Funkcja wątku BEZ synchronizacji.
        Operacja read → sleep(0) → write na shared_counter
        powoduje utratę aktualizacji (race condition).
        """
        partial_sum = 0
        for i in range(start, end):
            partial_sum += numbers[i]
            position = i - start + 1
            average = partial_sum / position

            shared_results.append({
                'thread_id': thread_id,
                'position': position,
                'partial_sum': partial_sum,
                'average': round(average, 2)
            })

            # Celowo nie-atomowa operacja read-modify-write
            current_sum = shared_counter['total_sum']
            current_count = shared_counter['count']
            time.sleep(0)  # wymuszenie przełączenia kontekstu
            shared_counter['total_sum'] = current_sum + numbers[i]
            shared_counter['count'] = current_count + 1

            if position % LOG_INTERVAL == 0 or position == (end - start):
                log_file.write(
                    f"Wątek {thread_id}: poz={position:>5}, "
                    f"suma_cząstkowa={partial_sum:>10}, "
                    f"średnia={average:>10.2f}\n"
                )

    # -----------------------------------------------------------------
    #  Uruchomienie
    # -----------------------------------------------------------------

    def _run(self, use_lock):
        """Wspólna logika dla obu wersji."""
        self._load_data()
        numbers = self.numbers
        n = len(numbers)
        chunk_size = n // NUM_THREADS

        shared_results = []
        shared_counter = {'total_sum': 0, 'count': 0}

        mode = "Z_LOCK" if use_lock else "BEZ_LOCK"
        log_name = f'log_thread_{mode.lower()}.txt'
        log_path = os.path.join(self.LOG_DIR, log_name)

        print("\n" + "-" * 60)
        if use_lock:
            print(f"  threading.Thread — Z synchronizacją (Lock) — {NUM_THREADS} wątki")
        else:
            print(f"  threading.Thread — BEZ synchronizacji — {NUM_THREADS} wątki")
            print("  [UWAGA] Brak Lock — możliwy wyścig wątków (race condition)!")
            print("  Proszę czekać... (sleep(0) wymusza przełączanie kontekstu)")
        print("-" * 60)

        results_lock = threading.Lock()
        counter_lock = threading.Lock()
        file_lock = threading.Lock()
        threads = []

        start_time = time.perf_counter()

        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"=== LOG: threading.Thread — {mode} ===\n")
            log_file.write(f"Wątków: {NUM_THREADS}, elementów: {n}\n\n")

            for t_id in range(NUM_THREADS):
                s = t_id * chunk_size
                e = s + chunk_size if t_id < NUM_THREADS - 1 else n

                if use_lock:
                    t = threading.Thread(
                        target=self._worker_sync,
                        args=(t_id + 1, numbers, s, e,
                              shared_results, results_lock,
                              shared_counter, counter_lock,
                              log_file, file_lock)
                    )
                else:
                    t = threading.Thread(
                        target=self._worker_unsync,
                        args=(t_id + 1, numbers, s, e,
                              shared_results, shared_counter,
                              log_file)
                    )
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            elapsed = (time.perf_counter() - start_time) * 1000
            expected = sum(numbers)

            # Podsumowanie do pliku
            log_file.write(f"\n{'='*50}\n")
            log_file.write(f"PODSUMOWANIE\n{'='*50}\n")
            log_file.write(f"  Suma ze shared_counter: {shared_counter['total_sum']}\n")
            log_file.write(f"  Licznik:                {shared_counter['count']} (oczekiwano: {n})\n")
            log_file.write(f"  Suma oczekiwana:        {expected}\n")

        # Wyniki cząstkowe wątków (ostatni wpis każdego)
        thread_final = {}
        for entry in shared_results:
            thread_final[entry['thread_id']] = entry

        print(f"\n  Wyniki cząstkowe wątków:")
        for tid in sorted(thread_final.keys()):
            e = thread_final[tid]
            print(f"    Wątek {tid}: suma = {e['partial_sum']:>10}, "
                  f"średnia = {e['average']:>10.2f}")

        actual = shared_counter['total_sum']
        actual_count = shared_counter['count']

        print(f"\n  Wpisów we wspólnej liście: {len(shared_results)}")
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
