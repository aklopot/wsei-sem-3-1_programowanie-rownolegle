# Laboratorium 3

Implementacja zadań z Lab 3 - rozbudowa aplikacji o metody wielowątkowości: Thread, ThreadPool, TPL, BackgroundWorker.

## Mapowanie C# na Python

| C# | Python |
|---|---|
| `Thread` | `threading.Thread` |
| `ThreadPool` | `multiprocessing.pool.ThreadPool` |
| `TPL` | `concurrent.futures.ThreadPoolExecutor` |
| `BackgroundWorker` | Symulacja z `threading` |

## Uruchomienie

```bash
# Utwórz środowisko
python -m venv .venv_lab3

# Aktywuj (Windows PowerShell)
.\.venv_lab3\Scripts\activate

# Zainstaluj pakiety
pip install -r requirements.txt

# Uruchom
python laboratorium_3.py
```

## Testy

```bash
pytest -v
```
