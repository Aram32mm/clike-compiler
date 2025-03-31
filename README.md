# C-like Compiler

A compiler that translates a simplified C-like language to CMA (Code for Virtual Abstract Machine) for execution on the VAM interpreter.

## 🌟 Features

- **Full Compiler Pipeline**: Lexer → Parser → Semantic Analyzer → Code Generator
- **C Language Subset**: Variables, functions, arrays, pointers, control structures
- **Robust Error Handling**: Detailed error messages for syntax and semantic issues
- **Visual Execution**: Execute generated code on the included VAM interpreter

## 📋 Prerequisites

- Python 3.6+
- Java Runtime Environment (for the VAM interpreter)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Aram32mm/clike-compiler.git
cd clike-compiler

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install .

# For development
pip install ".[dev]"
```

## 💻 Usage

```bash
# Basic compilation
python compiler.py your_source_file.c

# Specify output file
python compiler.py your_source_file.c -o output.cma

# Verbose mode (shows tokens, AST, etc.)
python compiler.py your_source_file.c --verbose
```

## 🏃 Running the compiled code

```bash
# Start the VAM interpreter
java -jar vam/vam.jar

# Then use the GUI:
# 1. VAM → Open Program...
# 2. Select your .cma file
# 3. Use the step/run buttons to execute
```

## 🧪 Testing

```bash
# Run all tests
pytest tests 

# Alternatively
python3 tests/run_tests.py

# Run specific test with output
pytest tests/test_lexer.py -s
```

## 📚 Compiler Components

- **Lexer**: Tokenizes source code using PLY
- **Parser**: Builds Abstract Syntax Tree
- **Symbol Table**: Manages variable/function scope and types
- **Semantic Analyzer**: Performs type checking and validation
- **Code Generator**: Produces CMA assembly code

## 🧩 Supported Language Features

- **Types**: int, float, char, void
- **Variables**: Declaration, initialization, assignment
- **Operators**: Arithmetic, comparison, logical, unary
- **Control Flow**: if/else, while, for, break/continue
- **Functions**: Definition, parameters, return values, recursion
- **Pointers**: Basic pointer operations
- **Scoping**: Block-level with variable shadowing

## 🔮 Future Work

The compiler is under development with plans to implement:
- Arrays support with proper indexing and memory management
- Function calls with parameter passing and return values
- Nested block scoping with correct variable visibility
- Pointer arithmetic and dereferencing
- Recursion support
- Comprehensive error handling and recovery

These features are tracked in the `tests/future_work/` directory with test cases that demonstrate the planned functionality.

## 📄 CMA Language

CMA is a simple stack-based assembly language with the following supported instructions:

### Constants and Memory
- `LOADC n` – Push constant `n` onto the stack  
- `LOADA addr` – Push value at memory address `addr`  
- `STOREA addr` – Store top of stack at address `addr`  
- `ALLOC n` – Reserve `n` memory slots

### Arithmetic
- `ADD`, `SUB`, `MUL`, `DIV`, `MOD` – Basic arithmetic on top two stack values  
- `NEG` – Negate top of stack

### Comparisons and Logic
- `EQ`, `NEQ`, `GE`, `LE` – Compare top two values  
- `AND`, `OR` – Logical operations  
- `NOT` – Logical negation

### Control Flow
- `JUMP addr` – Unconditional jump  
- `JUMPZ addr` – Jump if top of stack is zero

### Stack Operations
- `DUP` – Duplicate top of stack  
- `POP` – Discard top of stack

### Functions
- `ENTER n` – Enter a new stack frame of size `n`

### Miscellaneous
- `HALT` – Stop program execution

## 👨‍💻 Authors

- Jose Aram Mendez Gomez
- Ernesto Miranda Solis
- Weram Okhanian Saki
