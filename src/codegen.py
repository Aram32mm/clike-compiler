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
        self.label_counter = 0
        self.continue_labels = []
        self.break_labels = []
        self.verbose = verbose

    def generate(self, ast):
        """Generate code from the AST"""
        self.code = []
        self.variables = {}
        self.next_var_pos = 0

        if not isinstance(ast, list):
            raise TypeError(f"Expected AST to be a list of functions, got: {type(ast)}")

        for node in ast:
            self.visit(node)

        return '\n'.join(self.code)

    def visit(self, node):
        """Visit a node and dispatch to the appropriate method"""
        if not isinstance(node, tuple):
            raise TypeError(f"Invalid AST node (not a tuple): {node!r}")
        tag = node[0]
        method_name = f'visit_{tag}'
        visitor = getattr(self, method_name, self.generic_visit)
        if self.verbose:
            print(f"Visiting {tag} → {node}")
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node[0]}")

    def visit_FUNCTION(self, node):
        _, name, return_type, params, statements = node
        self.variables = {}
        self.next_var_pos = 0

        # self.code.append(f"{name}:")

        # Regular functions (with ENTER and RETURN)
        total_stack_space = len(params)
        self.code.append(f"ENTER {total_stack_space}")

        num_locals = self._count_locals(statements)
        if num_locals > 0:
            self.code.append(f"ALLOC {num_locals}")

        param_offset = 0
        for param in params:
            _, _, param_name = param
            self.variables[param_name] = param_offset
            param_offset += 1

        self.next_var_pos = len(params)

        for stmt in statements:
            self.visit(stmt)

        # Ensure functions always end with RETURN
        if return_type == 'void' and (not statements or statements[-1][0] != 'RETURN'):
            self.code.append("RETURN")

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
        if size_expr[0] != 'INTEGER':
            raise Exception("Only constant-size arrays supported for now")
        
        size = size_expr[1]
        base_addr = self.next_var_pos
        self.variables[name] = {
            "kind": "array",
            "base": base_addr,
            "size": size
        }
        self.next_var_pos += size

    def visit_ARRAY_ACCESS(self, node):
        _, name, index_expr = node
        if name not in self.variables:
            raise Exception(f"Undefined array: {name}")
        array_info = self.variables[name]
        base = array_info["base"]

        self.visit(index_expr)             # Push index
        self.code.append(f"LOADC {base}")  # Push base
        self.code.append("ADD")            # Compute address
        self.code.append("LOADA")          # Load from address

    def visit_ARRAY_ASSIGN(self, node):
        _, name, index_expr, value_expr = node
        if name not in self.variables:
            raise Exception(f"Undefined array: {name}")
        array_info = self.variables[name]
        base = array_info["base"]

        self.visit(index_expr)              # Push index
        self.code.append(f"LOADC {base}")   # Push base
        self.code.append("ADD")             # Compute address
        self.visit(value_expr)              # Push value
        self.code.append("STOREA")

    def visit_ASSIGN(self, node):
        _, name, expr = node
        if name not in self.variables:
            raise Exception(f"Undefined variable: {name}")
        offset = self.variables[name]
        self.visit(expr)
        self.code.append(f"STOREA {offset}    // Store result into variable '{name}'")

    def visit_CALL(self, node):
        _, func_name, args = node
        return_label = self._new_label("return_addr")
    
        # Push arguments in reverse order onto the stack
        for arg in reversed(args):
            self.visit(arg)

        # Push return address onto the stack (simulated)
        self.code.append(f"LOADC {return_label}")
        
        # Jump to function
        self.code.append(f"JUMP {func_name}")
        
        # Place return label here
        self.code.append(f"{return_label}:")

    def visit_RETURN(self, node):
        _, expr = node
        if expr is not None:
            self.visit(expr)
        self.code.append("RETURN    // Return the top of stack")

    def visit_IF(self, node):
        _, cond, then = node
        else_label = self._new_label("else")
        self.visit(cond)
        self.code.append(f"JUMPZ {else_label}    // Jump if condition is false")
        self.visit(then)
        self.code.append(f"{else_label}:")

    def visit_IF_ELSE(self, node, end_label=None):
        _, cond, then, otherwise = node
        else_label = self._new_label("else")
        
        # Create end_label if not provided (outermost IF_ELSE)
        if end_label is None:
            end_label = self._new_label("endif")

        # Condition check
        self.visit(cond)
        self.code.append(f"JUMPZ {else_label}    // Jump to else")

        # Then-block
        self.visit(then)
        self.code.append(f"JUMP {end_label}    // Skip else")

        # Else-block
        self.code.append(f"{else_label}:")
        
        # Recursive handling for chained IF_ELSE
        if otherwise[0] == 'IF_ELSE':
            self.visit_IF_ELSE(otherwise, end_label)
        else:
            self.visit(otherwise)

        # Only place end_label if it's the outermost IF_ELSE
        if end_label not in self.code[-1]:
            self.code.append(f"{end_label}:")


    def visit_WHILE(self, node):
        _, cond, body = node
        start_label = self._new_label("while_start")
        end_label = self._new_label("while_end")

        self.continue_labels.append(start_label)
        self.break_labels.append(end_label)

        self.code.append(f"{start_label}:")
        self.visit(cond)
        self.code.append(f"JUMPZ {end_label}    // Exit loop if condition is false")
        self.visit(body)
        self.code.append(f"JUMP {start_label}")
        self.code.append(f"{end_label}:")

        self.continue_labels.pop()
        self.break_labels.pop()


    def visit_FOR(self, node):
        _, init, cond, update, body = node
        self.visit(init)
        start_label = self._new_label("for_start")
        end_label = self._new_label("for_end")
        continue_label = self._new_label("for_continue")

        self.continue_labels.append(continue_label)
        self.break_labels.append(end_label)

        self.code.append(f"{start_label}:")
        self.visit(cond)
        self.code.append(f"JUMPZ {end_label}")
        self.visit(body)
        self.code.append(f"{continue_label}:")
        self.visit(update)
        self.code.append(f"JUMP {start_label}")
        self.code.append(f"{end_label}:")

        self.continue_labels.pop()
        self.break_labels.pop()

    def visit_BREAK(self, node):
        if not self.break_labels:
            raise Exception("BREAK used outside of loop")
        self.code.append(f"JUMP {self.break_labels[-1]}    // Break")

    def visit_CONTINUE(self, node):
        if not self.continue_labels:
            raise Exception("CONTINUE used outside of loop")
        self.code.append(f"JUMP {self.continue_labels[-1]}    // Continue")


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
            '==': 'EQ', '<': 'LE', '>': 'GE', '&&': 'AND', '||': 'OR'
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
        elif op == '!':
            self.code.append("NOT    // Logical NOT")
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
        
        entry = self.variables[name]

        if isinstance(entry, dict):
            if entry.get("kind") == "array":
                raise Exception(f"Cannot use array variable '{name}' as scalar")
            else:
                raise Exception(f"Unsupported variable structure for '{name}'")

        self.code.append(f"LOADA {entry}    // Load variable '{name}'")

    def _count_locals(self, statements):
        """Counts VAR_DECL and VAR_DECL_INIT nodes in the given statements."""
        count = 0

        def recurse(stmts):
            nonlocal count
            for stmt in stmts:
                tag = stmt[0]
                if tag in ('VAR_DECL', 'VAR_DECL_INIT'):
                    count += 1
                elif tag == 'BLOCK':
                    recurse(stmt[1])  # recurse into nested blocks
                elif tag in ('IF', 'IF_ELSE', 'WHILE', 'FOR'):
                    # recurse into potential nested statement(s)
                    for sub_stmt in stmt[1:]:
                        if isinstance(sub_stmt, tuple) and sub_stmt[0] in ('BLOCK', 'IF', 'IF_ELSE', 'WHILE', 'FOR'):
                            recurse([sub_stmt])
                        elif isinstance(sub_stmt, list):
                            recurse(sub_stmt)

        recurse(statements)
        return count


    def _new_label(self, base):
        label = f"{base}_{self.label_counter}"
        self.label_counter += 1
        return label
