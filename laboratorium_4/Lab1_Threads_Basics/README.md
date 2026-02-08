# Lab 4 — Zadanie 1: Sumowanie tablicy liczb

Aplikacja konsolowa porównująca sumowanie 10 000 liczb całkowitych z pliku CSV metodami:

1. **Sekwencyjnie** — prosta pętla
2. **threading.Thread** (2 i 8 wątków) — ograniczone przez GIL, brak realnego zysku
3. **multiprocessing.Pool** (2 i 8 procesów) — prawdziwa równoległość, zysk wydajnościowy

## Uruchomienie

```bash
cd laboratorium_4/Lab1_Threads_Basics
python Lab1_Threads_Basics.py
```

## Dane wejściowe

Plik `dane_wejsciowe/numbers1.csv` — 10 000 losowych liczb całkowitych rozdzielonych średnikiem.

## Struktura

```
Lab1_Threads_Basics/
├── Lab1_Threads_Basics.py          # Główny plik
├── README.md
└── src/
    ├── modules/
    │   ├── csv_loader.py                   # Ładowanie danych z CSV
    │   ├── thread_sum_calculator.py        # Wersja z threading.Thread
    │   └── multiprocess_sum_calculator.py  # Wersja z multiprocessing.Pool
    ├── utils/
    │   └── menu.py
    └── validators/
        └── input_validator.py
```
