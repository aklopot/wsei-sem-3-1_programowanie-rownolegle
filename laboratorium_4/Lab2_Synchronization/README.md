# Lab 4 — Zadanie 2: Synchronizacja wątków/procesów

Rozszerzenie zadania 1 o synchronizację dostępu do współdzielonych zasobów.

## Co robi aplikacja

- 4 wątki/procesy przetwarzają tablicę 10 000 liczb z pliku CSV
- Każdy wątek/proces zapisuje wyniki cząstkowe (sumę, średnią) do **wspólnej listy**
- **Logger** zapisuje postępy do wspólnego pliku tekstowego
- Cztery warianty:
  1. **threading.Thread + Lock** — poprawna synchronizacja
  2. **threading.Thread bez Lock** — race condition (sleep(0) wymusza przełączanie)
  3. **multiprocessing.Process + Lock** — poprawna synchronizacja (omija GIL)
  4. **multiprocessing.Process bez Lock** — race condition (brak GIL = większe straty)

## Uruchomienie

```bash
cd laboratorium_4/Lab2_Synchronization
python Lab2_Synchronization.py
```

## Pliki logów

Po uruchomieniu generowane są pliki:
- `log_thread_z_lock.txt` / `log_thread_bez_lock.txt`
- `log_process_z_lock.txt` / `log_process_bez_lock.txt`

## Struktura

```
Lab2_Synchronization/
├── Lab2_Synchronization.py
├── README.md
└── src/
    ├── modules/
    │   ├── csv_loader.py
    │   ├── thread_sync_calculator.py
    │   └── process_sync_calculator.py
    ├── utils/
    │   └── menu.py
    └── validators/
        └── input_validator.py
```
