# Lab 4 — Zadanie 4: Przetwarzanie obrazów

Równoległe przetwarzanie obrazów — filtr szarości (grayscale) piksel po pikselu.

## Co robi aplikacja

- Wczytuje min. 4 kolorowe obrazy z folderu `dane_wejsciowe/images/`
- Konwertuje na szarość wzorem: `gray = 0.299*R + 0.587*G + 0.114*B`
- Przetwarzanie ręczne, piksel po pikselu (celowo wolne, aby widać zysk z równoległości)
- Trzy opcje:
  1. **Sekwencyjne** — obraz po obrazie
  2. **Równoległe** — `ProcessPoolExecutor`, każdy obraz w osobnym procesie
  3. **Porównanie** — obie metody + zapis logu `processing_log.txt`
- Wyniki zapisywane do `wyniki/` z prefiksem `seq_` lub `par_`

## Uruchomienie

```bash
cd laboratorium_4/Lab4_ImageProcessing
```

Jeśli nie istnieje środowisko wirtualne `.venv_zad4`, utwórz je i aktywuj:

```bash
python -m venv .venv_zad4
```

Aktywacja (Windows PowerShell):
```bash
.\.venv_zad4\Scripts\Activate.ps1
```

Aktywacja (Windows CMD):
```bash
.venv_zad4\Scripts\activate.bat
```

Aktywacja (Linux/macOS):
```bash
source .venv_zad4/bin/activate
```

Instalacja zależności:
```bash
pip install -r requirements.txt
```

## Dane wejściowe

Umieść min. 4 kolorowe obrazy (`.png`, `.jpg`, `.jpeg`, `.bmp`) w folderze:
```
laboratorium_4/dane_wejsciowe/images/
```
Jeśli folder nie istnieje lub jest pusty, program wyświetli komunikat z instrukcją.

## Uruchomienie programu

```bash
python Lab4_ImageProcessing.py
```

## Struktura

```
Lab4_ImageProcessing/
├── Lab4_ImageProcessing.py
├── requirements.txt
├── README.md
├── wyniki/                  # folder wyjściowy
└── src/
    ├── modules/
    │   ├── image_loader.py      # ładowanie obrazów z folderu
    │   └── image_processor.py   # przetwarzanie sekw./równoległe + log
    ├── utils/
    │   └── menu.py
    └── validators/
        └── input_validator.py
```
