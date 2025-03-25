#!/usr/bin/env python3

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.variables = {}
        self.next_var_pos = 0

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
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node"""
        raise Exception(f"No visit method for {node[0]}")

    def visit_FUNCTION(self, node):
        """Generate code for a function"""
        _, func_name, statements = node

        # Count variables to allocate memory
        var_count = sum(1 for stmt in statements if stmt[0] == 'VAR_DECL')
        self.code.append(f"ALLOC {var_count}    // Allocate memory for {var_count} variables")

        # First process all variable declarations to allocate memory
        for stmt in statements:
            if stmt[0] == 'VAR_DECL':
                self.visit(stmt)

        # Then process all other statements
        for stmt in statements:
            if stmt[0] != 'VAR_DECL':
                self.visit(stmt)

        return self.code

    def visit_VAR_DECL(self, node):
        """Generate code for a variable declaration"""
        _, var_type, var_name = node
        self.variables[var_name] = self.next_var_pos
        self.next_var_pos += 1
        # No code emitted for declaration

    def visit_ASSIGN(self, node):
        """Generate code for an assignment statement"""
        _, var_name, expr = node
        if var_name not in self.variables:
            raise Exception(f"Undefined variable: {var_name}")

        # Evaluate expression
        self.visit(expr)

        # Store top of stack to variable slot
        var_pos = self.variables[var_name]
        self.code.append(f"STOREA {var_pos}    // Store result into variable '{var_name}'")

    def visit_RETURN(self, node):
        """Generate code for a return statement"""
        _, expr = node
        self.visit(expr)
        self.code.append("RETURN    // Return the top of stack")

    def visit_BINOP(self, node):
        """Generate code for a binary operation"""
        _, op, left, right = node

        self.visit(left)
        self.visit(right)

        if op == '+':
            self.code.append("ADD       // Add top two values")
        elif op == '-':
            self.code.append("SUB       // Subtract top two values")
        elif op == '*':
            self.code.append("MUL       // Multiply top two values")
        elif op == '/':
            self.code.append("DIV       // Divide top two values")
        else:
            raise Exception(f"Unsupported binary operator: {op}")

    def visit_UNARYOP(self, node):
        """Generate code for a unary operation"""
        _, op, operand = node
        self.visit(operand)

        if op == '-':
            self.code.append("NEG       // Negate top value")
        else:
            raise Exception(f"Unsupported unary operator: {op}")

    def visit_INTEGER(self, node):
        """Generate code for an integer literal"""
        _, value = node
        self.code.append(f"LOADC {value}    // Push {value} onto the stack")

    def visit_VARIABLE(self, node):
        """Generate code for a variable reference"""
        _, var_name = node
        if var_name not in self.variables:
            raise Exception(f"Undefined variable: {var_name}")
        var_pos = self.variables[var_name]
        self.code.append(f"LOADA {var_pos}    // Load variable '{var_name}' onto the stack")
