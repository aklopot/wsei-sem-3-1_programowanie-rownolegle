# Laboratorium 1 - Zadania

## 📋 Zawartość

Program zawiera kilka zadań obliczeniowych:

1. **Kalkulator Fibonacciego** - Oblicza elementy ciągu Fibonacciego
   - Zadanie 1: Pierwsze n elementów ciągu
   - Zadanie 2: Fragment ciągu od indeksu L1 przez L2 elementów

2. **Kalkulator Całki Numerycznej** - Oblicza całkę numeryczną metodą prostokątów
   - Zadanie 3: Całka funkcji f(x) = 1/2 * x na przedziale [0, 2]
   - Wykorzystuje metodę prostokątów (reguła punktu środkowego)
   - Wyświetla szczegółowe obliczenia dla każdego prostokąta

## 🚀 Szybki start

### 1️⃣ Utwórz środowisko wirtualne
```bash
python -m venv .venv_lab1
```

### 2️⃣ Aktywuj środowisko
**Windows:**
```bash
.\.venv_lab1\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv_lab1/Scripts/activate
```

### 3️⃣ Zainstaluj pakiety
```bash
pip install -r requirements.txt
```

### 4️⃣ Uruchom aplikację
```bash
python Laboratorium_1.py
```

### 5️⃣ Uruchom testy
```bash
pytest
```

### 6️⃣ Sprawdź pokrycie kodu
```bash
pytest --cov=src --cov-report=term-missing
```

---

**Deaktywacja środowiska:** `deactivate`
