# C-like Compiler

A compiler that translates a simplified C-like language to CMA (Code for Virtual Abstract Machine) for execution on the VAM interpreter.
 
**👉 [Zur deutschen Version](README.de.md)**

## 🌟 Features

- **Full Compiler Pipeline**: Lexer → Parser → Semantic Analyzer → Code Generator
- **C Language Subset**: Variables, functions, arrays, pointers, control structures
- **Robust Error Handling**: Detailed error messages for syntax and semantic issues
- **Visual Execution**: Execute generated code on the included VAM interpreter

## 📋 Prerequisites

- Python 3.6+
- Java Runtime Environment (for the VAM interpreter)

## ⚡ Executable Quickstart

```bash
# (macOS only) Remove quarantine flag if downloaded from the internet
xattr -d com.apple.quarantine ./clike-compiler

# Make sure the file is executable (Linux/macOS)
chmod +x ./clike-compiler

# Run the compiler on a source file
./clike-compiler file.c

```

## 🚀 Installation (from source)

```bash
# Clone the repository
git clone https://github.com/Aram32mm/clike-compiler.git
cd clike-compiler

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install --upgrade pip
pip install .

# For development/testing
pip install ".[dev]"
```

## ⚙️ Building a Standalone Executable (optional)

You can bundle the compiler into a standalone binary using **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile -n clike-compiler compiler.py
```

The result will be available in the `dist/` folder:

```bash
./dist/clike-compiler --help
```

You can now run this executable anywhere — **no Python installation needed**.

## 💻 Usage

### 🐍 With Python

```bash
# Compile a program
python compiler.py your_source_file.c

# Specify output file
python compiler.py your_source_file.c -o output.cma

# Verbose mode
python compiler.py your_source_file.c --verbose
```

### ⚙️ With the Executable

```bash
# Compile using the native executable (if built)
./clike-compiler your_source_file.c

# Optional flags
./clike-compiler your_source_file.c -o output.cma --verbose
```

Here’s a polished and professional version of that section:

---

## 🏃 Running the Compiled Code

### ▶️ Option 1: Using the External VAM GUI Interpreter

```bash
# Launch the VAM interpreter
java -jar vam/vam.jar
```

Then in the GUI:

1. Go to **VAM → Open Program...**
2. Select your `.cma` file
3. Use the **Step** or **Run** buttons to execute the program

> 💡 This is a visual tool ideal for inspecting execution step-by-step.

---

### 🧪 Option 2: Using the Built-in Python VM (for testing)

We provide a **Python-based prototype VM** for testing purposes.

- The core logic is located in:  
  `tests/utils/cma_instruction.py`

- To see how it’s used, check out the test runner:  
  `tests/utils/runner.py`

This internal VM allows automated testing of `.cma` output without needing the Java GUI. It's especially useful for continuous integration or debugging.

```bash
# Run integration tests with the VM
pytest tests/test_integration.py -s
```

## 🧪 Testing

```bash
# Run all tests
pytest tests 

# Alternatively
python3 tests/run_tests.py

# Run specific test with output
pytest tests/test_lexer.py -s

# Integration tests are parametrized, so if you want to do an integration test on one file do the following 
python3 tests/test_integration.py path_to_file/file_to_compile.c -s   
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

Planned improvements include:

- Full pointer arithmetic and dereferencing
- Recursive functions with call stack support
- Better error recovery
- CLI enhancements (`--dry-run`, `--no-semantic-checks`, etc.)
- Optimizations and dead code elimination

You can find test cases for upcoming features in the `tests/future_work/` directory.


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
