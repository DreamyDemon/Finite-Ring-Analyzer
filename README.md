# 🔍 Finite Ring Analyzer

A desktop app to test algebraic properties of finite rings, built with **Python** and **PyQt5**. Supports both built-in rings like **ℤ/nℤ** and fully custom rings via operation tables.


## ✨ Features

- ✅ Analyze whether a finite ring is:
  - **Commutative**
  - **Has a multiplicative identity**
  - **An integral domain**
  - **A division ring**
- 🔢 Supports both:
  - **ℤ/nℤ rings**: enter modulus and elements
  - **Custom rings**: define addition and multiplication tables manually
- 🚀 Fast Input Mode: type or paste multiple ring definitions in batch format
- 📦 Batch Mode: analyze multiple rings at once
- 📊 Detailed results per batch including:
  - True/False for each property
  - Counterexamples or explanations when a property fails
- 🖼️ Visualize addition and multiplication tables
- 💾 Export results to `.txt` or `.csv`
- ✅ Single `.exe` version available (built with PyInstaller)


## 🧪 Input Formats

### ℤ/nℤ Tab

#### Manual Mode
- Enter `n` (modulus)
- Enter elements to include (e.g. `0 2 4`)

#### Fast Input Mode (supports batches!)
- Example input:
```
3
0 2

4
0 1 3

2
0 1
```

#### Batch Mode
- Similar to manual mode, but can input many before analyzing

### Custom Tab

#### Manual Mode
- Specify `n`
- Fill in **addition** and **multiplication** tables

#### Fast Input Mode (supports batches!)

- Example input:
```
3
0 1 2
1 2 0
2 0 1
0 0 0
0 1 2
0 2 1

4
0 1 2 3
1 2 3 0
2 3 0 1
3 0 1 2
0 0 0 0
0 1 2 3
0 2 0 2
1 1 1 1

2
0 1
...
```

#### Batch Mode
- Similar to manual mode, but can input many before analyzing


## 📤 Export Format

Exports include:
- ✅/❌ for each ring property
- Counterexamples or notes, like:
  - `Zero divisors: (2, 3)`
  - `Missing inverse: 4`
  - `No multiplicative identity found`

Formats:
- **.csv** — for spreadsheets
- **.txt** — plain text


## ▶️ Running the App

### 💻 With Python

```bash
pip install -r requirements.txt
python main.py
```

### 📦 As Executable

If you're using the .exe build, simple launch:
```
FiniteRingAnalyzer.exe
```

### 🔧 Build Instructions

To make a standalone .exe (Windows):

Install PyInstaller:
```bash
pip install pyinstaller
```

Run this in your app folder:
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

This creates:
- `dist/main.exe — the final single-file app`
- `build/ — temp build files`
- `main.spec — config file (auto-generated)`

### 📦 Requirements

Python 3.8 or higher. Install dependencies:
```bash
pip install -r requirements.txt
```

Contents of requirements.txt:
```
PyQt5==5.15.11
PyQt5_sip==12.17.0
```

### 🧠 Notes

- Rings of size 1 (n = 1) are invalid
- Elements must be in [0, n-1]
- UI adjusts tables and visibility automatically
- Batch mode supports commas or spaces in input
- Error dialogs help identify input mistakes

### 📚 Educational Use

This app was developed as part of a Modern Algebra project. It helps test and visualize algebraic properties of finite rings interactively and efficiently.

### ✅ Status

All planned features implemented and tested:
- Full PyQt5 GUI
- ℤ/nℤ and Custom ring modes
- Fast + Batch input
- Table visualization
- Property checker with counterexamples
- Export to CSV/TXT
- Single-file .exe build
- Clean UI toggle and layout logic