import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tests.utils.cma_instruction import CMaInstruction

class CMaProgramParser:
    def __init__(self):
        pass

    def parse_lines(self, lines):
        instructions = []
        for line in lines:
            line.strip()
            if not line or line.startswith("//"):  # Skip empty lines and comments
                continue
            if "//" in line:
                line = line.split("//", 1)[0].strip()
            if line.endswith(":"):
                instructions.append(CMaInstruction("label", line[:-1]))
                continue
            parts = line.split()
            opcode = parts[0]
            # Leave operand as string if it's not a number
            if len(parts) > 1:
                operand_str = parts[1]
                try:
                    operand = int(operand_str)
                except ValueError:
                    operand = operand_str
            else:
                operand = None
            
            instructions.append(CMaInstruction(opcode, operand))
        return instructions

    def parse_file(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        return self.parse_lines(lines)

    def parse_string(self, program_string):
        lines = program_string.strip().split("\n")
        return self.parse_lines(lines)