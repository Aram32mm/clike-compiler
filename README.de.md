# C-like Compiler

Ein Compiler, der eine vereinfachte C-ähnliche Sprache in CMA übersetzt (Code für eine virtuelle abstrakte Maschine), zur Ausführung im VAM-Interpreter.

**👉 [English version](README.md)**

## 🌟 Funktionen

- **Komplette Compiler-Pipeline**: Lexer → Parser → Semantikanalyse → Code-Generierung
- **Teilmenge der C-Sprache**: Variablen, Funktionen, Arrays, Pointer, Kontrollstrukturen
- **Fehlertoleranz**: Aussagekräftige Fehlermeldungen bei Syntax- und Semantikfehlern
- **Visuelle Ausführung**: Ausführung des erzeugten Codes im VAM-Interpreter (GUI)

## 📋 Voraussetzungen

- Python 3.6 oder höher
- Java Runtime Environment (für den VAM-Interpreter)

## ⚡ Schnellstart für das Ausführbare Programm

```bash
# (nur macOS) Quarantäne-Flag entfernen, falls heruntergeladen
xattr -d com.apple.quarantine ./clike-compiler

# Datei ausführbar machen (Linux/macOS)
chmod +x ./clike-compiler

# Compiler auf eine C-Datei anwenden
./clike-compiler datei.c
```

## 🚀 Installation (aus dem Quellcode)

```bash
# Repository klonen
git clone https://github.com/Aram32mm/clike-compiler.git
cd clike-compiler

# Virtuelle Umgebung einrichten
python3 -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install --upgrade pip
pip install .

# Für Entwicklung/Tests
pip install ".[dev]"
```

## ⚙️ Erstellung einer eigenständigen ausführbaren Datei (optional)

Mit **PyInstaller** kannst du eine standalone-Binary erstellen:

```bash
pip install pyinstaller
pyinstaller --onefile -n clike-compiler compiler.py
```

Die erzeugte Datei befindet sich im `dist/` Verzeichnis:

```bash
./dist/clike-compiler --help
```

Diese Datei kann ohne Python-Installation auf anderen Rechnern ausgeführt werden.

## 💻 Verwendung

### 🐍 Mit Python

```bash
# Programm kompilieren
python compiler.py quellcode.c

# Ausgabedatei angeben
python compiler.py quellcode.c -o ausgabe.cma

# Mit Debug-/Verbose-Modus
python compiler.py quellcode.c --verbose
```

### ⚙️ Mit dem Ausführbaren

```bash
# Kompilierung mit der standalone-Binary
./clike-compiler quellcode.c

# Optional mit Flags
./clike-compiler quellcode.c -o ausgabe.cma --verbose
```

## 🏃 Ausführung des kompilierten Codes

### ▶️ Option 1: VAM GUI Interpreter verwenden

```bash
java -jar vam/vam.jar
```

Dann in der GUI:

1. **VAM → Open Program...**
2. `.cma`-Datei auswählen
3. Mit **Step** oder **Run** ausführen

> 💡 Ideal zur schrittweisen Ausführung und Analyse des Programms.

---

### 🧪 Option 2: Eingebauter Python-VM-Prototyp (nur für Tests)

Wir stellen einen **einfachen virtuellen Stack-Maschinen-Prototyp in Python** bereit:

- Kernlogik: `tests/utils/cma_instruction.py`
- Beispielnutzung: `tests/utils/runner.py`

Dies ist besonders nützlich für automatische Tests oder Continuous Integration.

```bash
pytest tests/test_integration.py -s
```

## 🧪 Tests

```bash
# Alle Tests ausführen
pytest tests

# Alternativ:
python3 tests/run_tests.py

# Spezifischen Test mit Ausgabe
pytest tests/test_lexer.py -s

# Einzelnen Integrationstest ausführen
python3 tests/test_integration.py pfad/zu/datei.c -s
```

## 📙 Compiler-Komponenten

- **Lexer**: Zerlegt Code in Tokens (PLY)
- **Parser**: Erstellt AST (Abstract Syntax Tree)
- **Symboltabelle**: Verwalten von Gültigkeit und Typen
- **Semantikanalyse**: Prüft Typen, Gültigkeit, etc.
- **Codegenerator**: Generiert CMA-Assembler-Code

## 🧰 Unterstützte Sprachfunktionen

- **Typen**: `int`, `float`, `char`, `void`
- **Variablen**: Deklaration, Initialisierung, Zuweisung
- **Operatoren**: Arithmetisch, logisch, Vergleich, unär
- **Kontrollstrukturen**: `if`, `else`, `while`, `for`, `break`, `continue`
- **Funktionen**: Definition, Parameter, Rückgabe, Rekursion
- **Arrays**: Statische Arrays mit Indexierung
- **Pointer**: Einfache Nutzung und Dereferenzierung
- **Blöcke/Scopes**: Sichtbarkeit von Variablen

## 🔮 Geplante Verbesserungen

- Volle Pointer-Arithmetik
- Rekursive Funktionen mit Stack-Verwaltung
- Fehlerbehandlung mit Recovery
- CLI-Erweiterungen (`--dry-run`, `--no-semantic-checks`, ...)
- Codeoptimierung & Dead-Code-Elimination

Geplante Features findest du unter `tests/future_work/` mit passenden Testfällen.

## 📄 CMA-Sprache (Abstract Machine)

### Konstanten und Speicher
- `LOADC n` – Konstante `n` auf den Stack legen
- `LOADA addr` – Wert von Speicheradresse laden
- `STOREA addr` – Wert auf Top of Stack speichern
- `ALLOC n` – `n` Speicherzellen reservieren

### Arithmetik
- `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
- `NEG` – Vorzeichen negieren

### Vergleich & Logik
- `EQ`, `NEQ`, `GE`, `LE`
- `AND`, `OR`, `NOT`

### Kontrollfluss
- `JUMP`, `JUMPZ`

### Stack-Operationen
- `DUP`, `POP`

### Funktionen
- `ENTER n`, `RETURN`, `HALT`

## 👨‍💼 Autoren

- Jose Aram Mendez Gomez
- Ernesto Miranda Solis
- Weram Okhanian Saki

