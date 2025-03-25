# C-like Language Compiler

## Overview
This project implements a compiler for a simplified C-like programming language. The compiler translates source code written in a C-like language to CMa code, which can be executed on the Virtual Abstract Machine (VAM).

## Features
- Lexical analysis using PLY (Python Lex-Yacc)
- Syntax parsing with operator precedence
- Code generation for basic C-like language
- Support for:
  - Integer variables
  - Variable assignment
  - Arithmetic operations (+, -, *, /)
  - Parenthesized expressions
  - Return statements
  - Basic function definition

## Project Structure
```
.
├── compiler.py         # Main compiler script
├── src/
│   ├── __init__.py     # Package marker
│   ├── lexer.py        # Lexical analyzer using PLY
│   ├── parser.py       # Syntax parser using PLY
│   └── codegen.py      # Code generator
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.6 or higher
- PLY (Python Lex-Yacc)

### Setup
1. Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  
```

2. Install dependencies:
```
pip install ply
```

## Usage
```
python compiler.py source_file.c [options]
```

Options:
- `-o, --output FILENAME`: Specify output file (default: input file with .cma extension)
- `--verbose`: Enable verbose output

## Limitations
This is a basic implementation with limited features:
- Only supports integers
- No control structures (if/else, loops)
- No function parameters or calls
- No error recovery
- No support for arrays or pointers