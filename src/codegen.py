#!/usr/bin/env python3
"""
CodeGenerator: Converts an AST from a C-like language into CMA assembly code.
Supports variables, arithmetic, return, control flow, and expressions.
"""

class CodeGenerator:
    def __init__(self, verbose=False):
        self.code = []
        self.variables = {}
        self.next_var_pos = 0
        self.verbose = verbose

    def generate(self, ast):
        """Generate code from the AST"""
        self.code = []
        self.variables = {}
        self.next_var_pos = 0
        self.visit(ast)
        return '\n'.join(self.code)

    def visit(self, node):
        """Visit a node and dispatch to the appropriate method"""
        method_name = f'visit_{node[0]}'
        visitor = getattr(self, method_name, self.generic_visit)
        if self.verbose:
            print(f"Visiting {node[0]} → {node}")
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node[0]}")

    def visit_FUNCTION(self, node):
        _, name, params, statements = node
        var_count = sum(1 for stmt in statements if stmt[0] in ('VAR_DECL', 'VAR_DECL_INIT', 'ARRAY_DECL'))
        self.code.append(f"ALLOC {var_count}    // Allocate memory for {var_count} variables")
        for stmt in statements:
            if stmt[0] in ('VAR_DECL', 'VAR_DECL_INIT', 'ARRAY_DECL'):
                self.visit(stmt)
        for stmt in statements:
            if stmt[0] not in ('VAR_DECL', 'VAR_DECL_INIT', 'ARRAY_DECL'):
                self.visit(stmt)

    def visit_VAR_DECL(self, node):
        _, t, name = node
        self.variables[name] = self.next_var_pos
        self.next_var_pos += 1

    def visit_VAR_DECL_INIT(self, node):
        _, t, name, expr = node
        self.variables[name] = self.next_var_pos
        var_pos = self.next_var_pos
        self.next_var_pos += 1
        self.visit(expr)
        self.code.append(f"STOREA {var_pos}    // Initialize variable '{name}'")

    def visit_ARRAY_DECL(self, node):
        _, t, name, size_expr = node
        self.visit(size_expr)  # Size evaluated but ignored for now
        self.variables[name] = self.next_var_pos
        self.next_var_pos += 1  # Simplified memory allocation model

    def visit_ASSIGN(self, node):
        _, name, expr = node
        if name not in self.variables:
            raise Exception(f"Undefined variable: {name}")
        self.visit(expr)
        self.code.append(f"STOREA {self.variables[name]}    // Store result into variable '{name}'")

    def visit_RETURN(self, node):
        _, expr = node
        if expr is not None:
            self.visit(expr)
        self.code.append("RETURN    // Return the top of stack")

    def visit_IF(self, node):
        _, cond, then = node
        self.visit(cond)
        label = self._new_label("else")
        self.code.append(f"JUMPZ {label}    // Jump if condition is false")
        self.visit(then)
        self.code.append(f"{label}:")

    def visit_IF_ELSE(self, node):
        _, cond, then, otherwise = node
        else_label = self._new_label("else")
        end_label = self._new_label("endif")
        self.visit(cond)
        self.code.append(f"JUMPZ {else_label}    // Jump to else")
        self.visit(then)
        self.code.append(f"JUMP {end_label}    // Skip else")
        self.code.append(f"{else_label}:")
        self.visit(otherwise)
        self.code.append(f"{end_label}:")

    def visit_WHILE(self, node):
        _, cond, body = node
        start = self._new_label("while_start")
        end = self._new_label("while_end")
        self.code.append(f"{start}:")
        self.visit(cond)
        self.code.append(f"JUMPZ {end}    // Exit loop if false")
        self.visit(body)
        self.code.append(f"JUMP {start}")
        self.code.append(f"{end}:")

    def visit_FOR(self, node):
        _, init, cond, update, body = node
        self.visit(init)
        start = self._new_label("for_start")
        end = self._new_label("for_end")
        self.code.append(f"{start}:")
        self.visit(cond)
        self.code.append(f"JUMPZ {end}")
        self.visit(body)
        self.visit(update)
        self.code.append(f"JUMP {start}")
        self.code.append(f"{end}:")

    def visit_BLOCK(self, node):
        _, stmts = node
        for stmt in stmts:
            self.visit(stmt)

    def visit_BINOP(self, node):
        _, op, left, right = node
        self.visit(left)
        self.visit(right)
        ops = {
            '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', '%': 'MOD',
            '==': 'EQ', '<': 'LE', '>': 'GE'
        }
        if op in ops:
            self.code.append(f"{ops[op]}    // Binary {op}")
        elif op == '!=':
            self.code.append("EQ")
            self.code.append("NOT    // Simulated !=")
        elif op == '<=':
            self.code.append("GE")
            self.code.append("NOT    // Simulated <=")
        elif op == '>=':
            self.code.append("LE")
            self.code.append("NOT    // Simulated >=")
        else:
            raise Exception(f"Unsupported binary operator: {op}")

    def visit_UNARYOP(self, node):
        _, op, expr = node
        self.visit(expr)
        if op == '-':
            self.code.append("NEG    // Unary negation")
        else:
            raise Exception(f"Unsupported unary operator: {op}")

    def visit_INTEGER(self, node):
        _, val = node
        self.code.append(f"LOADC {val}    // Push {val} onto the stack")

    def visit_FLOAT(self, node):
        _, val = node
        self.code.append(f"LOADC {val}    // Push float {val} onto the stack")

    def visit_STRING(self, node):
        _, val = node
        self.code.append(f"LOADC \"{val}\"    // Push string")

    def visit_CHAR(self, node):
        _, val = node
        self.code.append(f"LOADC '{val}'    // Push char")

    def visit_VARIABLE(self, node):
        _, name = node
        if name not in self.variables:
            raise Exception(f"Undefined variable: {name}")
        self.code.append(f"LOADA {self.variables[name]}    // Load variable '{name}'")

    def _new_label(self, base):
        count = len([line for line in self.code if line.startswith(base)])
        return f"{base}_{count}"
