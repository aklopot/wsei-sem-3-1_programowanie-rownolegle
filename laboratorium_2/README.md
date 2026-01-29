# Laboratorium 2 - Zadania

## 📋 Zawartość

Program zawiera zadania z programowania równoległego:

1. **Zadanie 1** - Obliczanie całki metodą trapezów (jednowątkowo)
2. **Zadanie 2** - Obliczanie całki równolegle (threading.Thread)
3. **Zadanie 3** - Wybór metody (Thread vs ThreadPoolExecutor)

## 🚀 Szybki start

### 1️⃣ Utwórz środowisko wirtualne
```bash
python -m venv .venv_lab2
```

### 2️⃣ Aktywuj środowisko
**Windows (PowerShell):**
```powershell
.\.venv_lab2\Scripts\activate
```

**Windows (Git Bash / MINGW64):**
```bash
source .venv_lab2/Scripts/activate
```

**Linux/Mac:**
```bash
source .venv_lab2/bin/activate
```

### 3️⃣ Zainstaluj pakiety
```bash
pip install -r requirements.txt
```

### 4️⃣ Uruchom aplikację
```bash
python laboratorium_2.py
```

### 5️⃣ Uruchom testy
```bash
pytest
```

### 6️⃣ Uruchom testy z szczegółami
```bash
pytest -v
```

### 7️⃣ Sprawdź pokrycie kodu
```bash
pytest --cov=src --cov-report=term-missing
```
