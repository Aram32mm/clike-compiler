class CMaInstruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode.lower()
        self.operand = operand

class CMaInstructionProcessor:
    def __init__(self, verbose = False):
        self.stack = []
        self.memory = [0] * 1000
        self.pc = 0
        self.instructions = []
        self.labels = {}
        self.return_value = None
        self.running = False
        self.verbose = verbose

    def load_instructions(self, instruction_list):
        raw_index = 0
        for instr in instruction_list:
            if instr.opcode == "label":
                self.labels[instr.operand] = raw_index
            else:
                self.instructions.append(instr)
                raw_index += 1

    def step(self):
        if (self.pc >= len(self.instructions)):
            self.running = False
            return
        
        instruction = self.instructions[self.pc]
        self.pc += 1

        if self.verbose:
            print(f"[PC={self.pc-1}] {instruction.opcode.upper()} {instruction.operand if instruction.operand is not None else ''}")
            print(f"    Stack: {self.stack}")
            print(f"    Memory (first 10): {self.memory[:10]}")

        # Dispatch based on opcode
        method = getattr(self, f"op_{instruction.opcode.lower()}", None)
        if method:
            method(instruction.operand)
        else:
            raise Exception(f"Unknown instruction: {instruction.opcode.upper()}")

    def run(self):
        self.running = True
        while self.running:
            self.step()

    # === Instruction Implementations ===

    def op_alloc(self, size):
        size = int(size)
        for _ in range(size):
            self.stack.append(0)
    
    def op_loadc(self, value):
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
            self.stack.append(int(value))
        elif isinstance(value, str):
            # Character literal check
            if len(value) == 3 and value.startswith("'") and value.endswith("'"):
                self.stack.append(ord(value[1]))
            else:
                try:
                    # Try to parse as float
                    self.stack.append(float(value))
                except ValueError:
                    if value in self.labels:
                        self.stack.append(self.labels[value])
                    else:
                        raise ValueError(f"Invalid LOADC operand: '{value}'")
        elif isinstance(value, float):
            self.stack.append(value)
        else:
            raise ValueError(f"Invalid LOADC operand: '{value}'")

    def op_call(self, function_name):
        # Save return address (current PC)
        self.stack.append(self.pc)  # Save where to return to
        
        # Jump to function
        if function_name in self.labels:
            self.pc = self.labels[function_name]
        else:
            raise RuntimeError(f"Unknown function: {function_name}")

    def op_enter(self, size):
        size = int(size)
        # Ensure memory is large enough
        if len(self.memory) < size:
            self.memory.extend([0] * (size - len(self.memory)))

    def op_return(self, _=None):
        if not self.stack:
            return_value = 0
        else:
            return_value = self.stack[-1]  # Keep on stack but remember it
        
        self.running = False
        self.return_value = return_value

    def op_loada(self, address):
        address = int(address)
        self.stack.append(self.memory[address])
    
    def op_storea(self, address):
        address = int(address)
        self.memory[address] = self.stack.pop()

    def op_add(self, _=None):
        self._binary_op(lambda a, b: a + b, "ADD")

    def op_sub(self, _=None):
        self._binary_op(lambda a, b: a - b, "SUB")

    def op_mul(self, _=None):
        self._binary_op(lambda a, b: a * b, "MUL")

    def op_div(self, _=None):
        self._binary_op(lambda a, b: a // b if b != 0 else 0, "DIV")

    def op_mod(self, _=None):
        self._binary_op(lambda a, b: a % b if b != 0 else 0, "MOD")

    def op_eq(self, _=None):
        self._binary_op(lambda a, b: 1 if a == b else 0, "EQ")
    
    def op_neg(self, _=None):
        if not self.stack:
                raise RuntimeError("Stack underflow on NEG")
        value = self.stack.pop()
        self.stack.append(-value)
    
    def op_and(self, _=None):
        self._binary_op(lambda a, b: 1 if a and b else 0, "AND")

    def op_or(self, _=None):
        self._binary_op(lambda a, b: 1 if a or b else 0, "OR")

    def op_not(self, _=None):
        if not self.stack:
            raise RuntimeError("Stack underflow on NOT")
        value = self.stack.pop()
        self.stack.append(1 if value == 0 else 0)
    
    def op_ge(self, _=None):
        self._binary_op(lambda a, b: 1 if a > b else 0, "GE")
    
    def op_le(self, _=None):
        self._binary_op(lambda a, b: 1 if a < b else 0, "LE")

    def op_jump(self, label):
        if label not in self.labels:
            raise Exception(f"Undefined label: {label}")
        self.pc = self.labels[label]

    def op_jumpz(self, label):
        if label not in self.labels:
            raise Exception(f"Undefined label: {label}")
        if not self.stack:
            raise RuntimeError("Stack underflow on JUMPZ")
        condition = self.stack.pop()
        if condition == 0:
            self.pc = self.labels[label]

    # === Helpers ===

    def _binary_op(self, func, name):
        if len(self.stack) < 2:
            raise RuntimeError(f"Stack underflow on {name}")
        b = self.stack.pop()
        a = self.stack.pop()
        result = func(a, b)
        self.stack.append(result)

    def _check_memory_bounds(self, index):
        if not (0 <= index < len(self.memory)):
            raise IndexError(f"Memory access out of bounds at index {index}")
