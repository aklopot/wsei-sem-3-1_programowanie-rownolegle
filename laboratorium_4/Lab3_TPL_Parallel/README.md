# Lab 4 — Zadanie 3: TPL / Parallel (concurrent.futures)

Odpowiednik C# Task Parallel Library (TPL) w Pythonie.

## Co robi aplikacja

- **Parallel.For** — sumowanie tablicy 10 000 liczb z `numbers1.csv` przy użyciu `ProcessPoolExecutor` (4 i 8 workerów)
- **Parallel.ForEach** — równoległe przetwarzanie 4 plików CSV (`numbers1-4.csv`) — każdy plik w oddzielnym procesie
- **Pełny benchmark** — porównanie wszystkich metod z zadań 1-3 (sekwencyjna, threading, multiprocessing.Pool, Parallel.For, Parallel.ForEach) z zapisem wyników do `benchmark_log.txt`

## Uruchomienie

```bash
cd laboratorium_4/Lab3_TPL_Parallel
python Lab3_TPL_Parallel.py
```

## Dane wejściowe

```
dane_wejsciowe/
├── numbers1.csv
├── numbers2.csv
├── numbers3.csv
└── numbers4.csv
```

## Struktura

```
Lab3_TPL_Parallel/
├── Lab3_TPL_Parallel.py
├── README.md
└── src/
    ├── modules/
    │   ├── csv_loader.py
    │   ├── parallel_for_calculator.py      # Parallel.For
    │   ├── parallel_foreach_calculator.py  # Parallel.ForEach
    │   └── benchmark_runner.py             # Pełny benchmark + log
    ├── utils/
    │   └── menu.py
    └── validators/
        └── input_validator.py
```
