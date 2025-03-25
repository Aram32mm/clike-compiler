# C-like Language to VAM Compiler

A compiler that translates a simplified C-like language to CMA code for execution on the Virtual Abstract Machine (VAM).

## Overview

This project implements a complete compiler pipeline for a subset of the C programming language. The compiler translates source code into CMA (Code for the Virtual Abstract Machine), which can be executed on the VAM interpreter.

## Features

- Full compiler pipeline implementation:
  - Lexical analysis using PLY (Python Lex-Yacc)
  - Syntax parsing with operator precedence
  - Abstract Syntax Tree (AST) generation
  - Code generation targeting VAM architecture
- Supported C language features:
  - Integer variables and arithmetic operations
  - Variable declarations and assignments
  - Expressions with correct operator precedence
  - Unary operations
  - Basic function structure
  - Return statements

## Project Structure

```
c_to_vam_compiler/
├── compiler.py           # Main compiler entry point
├── setup.py              # Package setup script
├── README.md             # Documentation
├── .gitignore            # Git ignore file
├── src/                  # Source code for the compiler
│   ├── __init__.py       # Package marker
│   ├── lexer.py          # Lexical analyzer
│   ├── parser.py         # Syntax parser
│   └── codegen.py        # Code generator
├── examples/             # Example C programs
│   ├── simple.c          # Simple example program
│   ├── simple.cma        # Compiled output for simple.c
│   ├── complex.c         # More complex example program
│   └── complex.cma       # Compiled output for complex.c
├── cma_examples/         # Additional CMA examples
└── vam/                  # VAM interpreter
    ├── vam.jar           # VAM Java implementation
    ├── vam.sh            # Unix/Linux/macOS launcher
    └── vam.bat           # Windows launcher
```

## Installation

### Prerequisites

- Python 3.6 or higher
- PLY (Python Lex-Yacc) library
- Java Runtime Environment (for running the VAM interpreter)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/c_to_vam_compiler.git
   cd c_to_vam_compiler
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Unix/Linux/macOS
   source venv/bin/activate
   # On Windows
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Compiling C Code

```bash
python compiler.py input_file.c [-o output_file.cma] [--verbose]
```

Options:
- `-o, --output FILENAME`: Specify output file (default: input file with .cma extension)
- `--verbose`: Enable verbose output

### Running Compiled Code

To run the compiled CMA code on the VAM interpreter:

```bash
# On Unix/Linux/macOS
./vam/vam.sh output_file.cma

# On Windows
vam\vam.bat output_file.cma
```

## Examples

### Simple Example

```c
// simple.c
int main() {
    int a;
    a = -5;
    return a;
}
```

Compiling this example:
```bash
python compiler.py examples/simple.c
```

### Complex Example (Work in Progress)

More complex examples are available in the `examples/` directory.

## Development

### Running Tests

To run tests (once implemented):
```bash
python -m unittest discover tests
```

### Adding New Features

The compiler pipeline can be extended by modifying:
- `lexer.py` - Add new token types
- `parser.py` - Add grammar rules for new language constructs
- `codegen.py` - Add code generation for new AST nodes

## Limitations

Current limitations of the compiler:
- Only supports integer type
- No control structures (if/else, loops)
- No function parameters or function calls
- No arrays or pointers
- Limited error handling and recovery

## License

[Specify your license here]

## Acknowledgments

- This project was created as part of the Compiler Construction course at HTW Saar.
- The VAM (Virtual Abstract Machine) was provided by [specify source if applicable].