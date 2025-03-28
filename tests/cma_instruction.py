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
        self.running = False
        self.verbose = verbose

    def load_instructions(self, instruction_list):
        self.instructions = instruction_list
        self.pc = 0

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
        self.memory = [0] * int(size)
    
    def op_loadc(self, value):
        self.stack.append(int(value))
    
    def op_storea(self, index):
        index = int(index)
        self._check_memory_bounds(index)
        if not self.stack:
            raise RuntimeError("Stack underflow on STOREA")
        self.memory[index] = self.stack.pop()

    def op_loada(self, index):
        index = int(index)
        self._check_memory_bounds(index)
        self.stack.append(self.memory[index])
    
    def op_add(self, _=None):
        self._binary_op(lambda a, b: a + b, "ADD")

    def op_sub(self, _=None):
        self._binary_op(lambda a, b: a - b, "SUB")

    def op_mul(self, _=None):
        self._binary_op(lambda a, b: a * b, "MUL")

    def op_div(self, _=None):
        self._binary_op(lambda a, b: a // b if b != 0 else 0, "DIV")

    def op_return(self, _=None):
        if not self.stack:
            print("Warning: RETURN called on empty stack.")
            self.running = False
            return
        result = self.stack.pop()
        print(f"\n✅ Returned: {result}")
        self.running = False
    
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
