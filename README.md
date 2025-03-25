# C-like Language to VAM Compiler

A compiler that translates a simplified C-like language to CMA code for execution on the Virtual Abstract Machine (VAM).

## Overview

This project implements a complete compiler pipeline for a subset of the C programming language. The compiler translates source code into CMA (Code for the Virtual Abstract Machine), which can be executed on the VAM interpreter.


## Installation

### Prerequisites

- Python 3.6 or higher
- PLY (Python Lex-Yacc) library
- Java Runtime Environment (for running the VAM interpreter)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Aram32mm/clike-compiler.git
   cd c_to_vam_compiler
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   
   ```
   
4. Verify installation:
   ```bash
   python3 compiler.py resources/file.c
   ```

    Other scripts:

    Run And Compile All Resources
   ```bash
   chmod +x scripts/compile_all.sh
   ./scripts/compile_all.sh
   ```


