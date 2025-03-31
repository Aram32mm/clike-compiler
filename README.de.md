# C-like Compiler

Ein Compiler, der eine vereinfachte C-ähnliche Sprache in CMA (Code für Virtuelle Abstrakte Maschine) übersetzt, zur Ausführung auf dem VAM-Interpreter.

## 🌟 Features

- **Vollständige Compiler-Pipeline**: Lexer → Parser → Semantischer Analysator → Code-Generator
- **C-Sprachuntergruppe**: Variablen, Funktionen, Arrays, Zeiger, Kontrollstrukturen
- **Robuste Fehlerbehandlung**: Detaillierte Fehlermeldungen für Syntax- und semantische Probleme
- **Visuelle Ausführung**: Ausführung des generierten Codes auf dem integrierten VAM-Interpreter

## 📋 Voraussetzungen

- Python 3.6+
- Java Runtime Environment (für den VAM-Interpreter)

## 🚀 Installation

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

# Für die Entwicklung
pip install ".[dev]"
```

## 💻 Verwendung

```bash
# Grundlegende Kompilierung
python compiler.py deine_quelldatei.c

# Ausgabedatei angeben
python compiler.py deine_quelldatei.c -o ausgabe.cma

# Ausführlicher Modus (zeigt Tokens, AST usw.)
python compiler.py deine_quelldatei.c --verbose
```

## 🏃 Ausführen des kompilierten Codes

```bash
# Starten des VAM-Interpreters
java -jar vam/vam.jar

# Dann die GUI verwenden:
# 1. VAM → Programm öffnen...
# 2. Wähle deine .cma-Datei aus
# 3. Verwende die Schritt/Ausführen-Schaltflächen zum Ausführen
```

## 🧪 Testen

```bash
# Alle Tests ausführen
pytest tests 

# Alternativ
python3 tests/run_tests.py

# Bestimmten Test mit Ausgabe ausführen
pytest tests/test_lexer.py -s
```

## 📚 Compiler-Komponenten

- **Lexer**: Tokenisiert Quellcode mit PLY
- **Parser**: Erstellt abstrakten Syntaxbaum
- **Symboltabelle**: Verwaltet Variablen-/Funktionsbereich und Typen
- **Semantischer Analysator**: Führt Typprüfung und Validierung durch
- **Code-Generator**: Erzeugt CMA-Assembly-Code

## 🧩 Unterstützte Sprachfunktionen

- **Typen**: int, float, char, void
- **Variablen**: Deklaration, Initialisierung, Zuweisung
- **Operatoren**: Arithmetisch, Vergleich, logisch, unär
- **Kontrollfluss**: if/else, while, for, break/continue
- **Funktionen**: Definition, Parameter, Rückgabewerte, Rekursion
- **Zeiger**: Grundlegende Zeigeroperationen
- **Gültigkeitsbereich**: Blockebene mit Variablenüberschattung

## 🔮 Zukünftige Arbeit

Der Compiler befindet sich in der Entwicklung mit Plänen zur Implementierung von:
- Arrays-Unterstützung mit richtiger Indexierung und Speicherverwaltung
- Funktionsaufrufe mit Parameterübergabe und Rückgabewerten
- Verschachtelte Blockbereiche mit korrekter Variablensichtbarkeit
- Zeigerarithmetik und Dereferenzierung
- Rekursionsunterstützung
- Umfassende Fehlerbehandlung und -wiederherstellung

Diese Funktionen werden im Verzeichnis `tests/future_work/` mit Testfällen verfolgt, die die geplante Funktionalität demonstrieren.

## 📄 CMA-Sprache

CMA ist eine einfache stapelbasierte Assemblersprache mit den folgenden unterstützten Anweisungen:

### Konstanten und Speicher
- `LOADC n` – Konstante `n` auf den Stapel legen  
- `LOADA addr` – Wert an Speicheradresse `addr` auf den Stapel legen  
- `STOREA addr` – Oberstes Element des Stapels an Adresse `addr` speichern  
- `ALLOC n` – `n` Speicherplätze reservieren

### Arithmetik
- `ADD`, `SUB`, `MUL`, `DIV`, `MOD` – Grundlegende Arithmetik auf den oberen zwei Stapelwerten  
- `NEG` – Negiere Stapelspitze

### Vergleiche und Logik
- `EQ`, `NEQ`, `GE`, `LE` – Vergleiche die oberen zwei Werte  
- `AND`, `OR` – Logische Operationen  
- `NOT` – Logische Negation

### Kontrollfluss
- `JUMP addr` – Unbedingter Sprung  
- `JUMPZ addr` – Springe, wenn Stapelspitze Null ist

### Stapeloperationen
- `DUP` – Dupliziere Stapelspitze  
- `POP` – Entferne Stapelspitze

### Funktionen
- `ENTER n` – Betrete einen neuen Stapelrahmen der Größe `n`

### Verschiedenes
- `HALT` – Stoppe Programmausführung

## 👨‍💻 Autoren

- Jose Aram Mendez Gomez
- Ernesto Miranda Solis
- Weram Okhanian Saki