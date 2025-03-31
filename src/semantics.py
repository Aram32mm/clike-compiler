#!/usr/bin/env python3
"""
SemanticAnalyzer: Performs semantic analysis on the AST of a C-like language.
Checks for undeclared variables, redeclarations, function calls, and manages scopes.
"""

from src.symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self, verbose=False):
        self.symbols = SymbolTable()
        self.errors = []
        self.verbose = verbose
        self.current_function_return_type = None
        self.loop_depth = 0

    # Two pass architecture for function declarations
    def analyze(self, ast):
        if not isinstance(ast, list):
            ast = [ast]
        
        # First pass: declare all functions
        for node in ast:
            if node[0] == 'FUNCTION':
                _, name, return_type, params, _ = node
                if not all(len(param) == 3 and param[0] == 'PARAM' for param in params):
                    self.error(f"Malformed parameter list in function '{name}'")
                    continue
                param_types = [param[1] for param in params]
                if self.symbols.lookup(name):
                    self.error(f"Function '{name}' already declared")
                else:
                    self.symbols.declare(name, return_type, 'func', extra={'params': param_types})
   
        # Second pass: full semantic analysis
        for node in ast:
            self.visit(node)

        return self.errors

    def error(self, message):
        self.errors.append(message)
        if self.verbose:
            print(f"❌ Semantic error: {message}")

    def visit(self, node):
        if node is None:
            return None
        kind = node[0]
        method = getattr(self, f"visit_{kind.lower()}", None)
        if method:
            if self.verbose:
                print("✅ Found method:", method.__name__)
            return method(node)
        else:
            self.error(f"No handler for AST node '{kind}'")
            return None

    def visit_function(self, node):
        _, name, return_type, params, body = node
        if not all(len(param) == 3 and param[0] == 'PARAM' for param in params):
            self.error(f"Malformed parameter list in function '{name}'")
            return
        self.current_function_return_type = return_type
        self.symbols.push_scope()
        for _, t, n in params:
            self.symbols.declare(n, t, 'param')
        for stmt in body:
            self.visit(stmt)
        self.symbols.pop_scope()
        self.current_function_return_type = None

    def visit_var_decl(self, node):
        _, t, name = node
        if name in self.symbols.scopes[-1]:
            self.error(f"Variable '{name}' already declared")
        else:
            self.symbols.declare(name, t, 'var')
        
    def visit_var_decl_init(self, node):
        _, t, name, expr = node
        if name in self.symbols.scopes[-1]: # Only check current scope
            self.error(f"Variable '{name}' already declared")
        else:
            expr_type = self.visit(expr)
            if expr_type and expr_type != t:
                self.error(f"Type mismatch in declaration: {t} {name} = {expr_type}")
            self.symbols.declare(name, t, 'var')

    def visit_array_decl(self, node):
        _, t, name, size_expr = node
        if name in self.symbols.scopes[-1]:  # Only check current scope
            self.error(f"Array '{name}' already declared")
        else:
            size_type = self.visit(size_expr)
            if size_type != 'int':
                self.error(f"Array size must be an integer, got '{size_type}'")
            size_val = size_expr[1]  # assuming size_expr is ('INTEGER', N)
            self.symbols.declare(name, t, 'array', extra={'size': size_val})

    def visit_assign(self, node):
        _, name, expr = node
        var_info = self.symbols.lookup(name)
        if not var_info:
            self.error(f"Assignment to undeclared variable '{name}'")
            return None
        expr_type = self.visit(expr)
        if expr_type and expr_type != var_info.type:
            self.error(f"Type mismatch in assignment to '{name}': {var_info.type} = {expr_type}")
        return expr_type

    def visit_return(self, node):
        _, expr = node
        if expr is not None:
            return_type = self.visit(expr)
            if return_type is None:
                return # Avoid cascade if expr failed
            if self.current_function_return_type and return_type != self.current_function_return_type:
                self.error(f"Return type mismatch: expected {self.current_function_return_type}, got {return_type}")
            return
        elif self.current_function_return_type != 'void':
            self.error(f"Return type mismatch: expected {self.current_function_return_type}, got void")
        return None

    def visit_if(self, node):
        _, cond, then = node
        self.visit(cond)
        self.visit(then)
        return None

    def visit_if_else(self, node):
        _, cond, then, otherwise = node
        self.visit(cond)
        self.visit(then)
        self.visit(otherwise)

    def visit_while(self, node):
        _, cond, body = node
        self.visit(cond)
        self.loop_depth += 1
        self.visit(body)
        self.loop_depth -= 1

    def visit_for(self, node):
        _, init, cond, update, body = node
        self.symbols.push_scope()
        self.visit(init)
        self.visit(cond)
        self.visit(update)
        self.loop_depth += 1
        self.visit(body)
        self.loop_depth -= 1
        self.symbols.pop_scope()

    def visit_break(self, node):
        if self.loop_depth == 0:
            self.error("BREAK used outside of loop")

    def visit_continue(self, node):
        if self.loop_depth == 0:
            self.error("CONTINUE used outside of loop")

    def visit_block(self, node):
        _, stmts = node
        self.symbols.push_scope()
        for stmt in stmts:
            self.visit(stmt)
        self.symbols.pop_scope()

    def visit_call(self, node):
        _, func_name, args = node
        info = self.symbols.lookup(func_name)
        if not info:
            self.error(f"Call to undeclared function '{func_name}'")
            return None
        if info.kind == 'func':
            expected = info.extra.get('params', [])
            if len(expected) != len(args):
                self.error(f"Function '{func_name}' called with wrong number of arguments: expected {len(expected)}, got {len(args)}")
                return None
            for i, (expected_type, arg_expr) in enumerate(zip(expected, args)):
                actual_type = self.visit(arg_expr)
                if actual_type != expected_type:
                    self.error(f"Type mismatch in argument {i+1} of call to '{func_name}': expected {expected_type}, got {actual_type}")
            return info.type
        else:
            self.error(f"'{func_name}' is not callable")
            return None

    def visit_array_access(self, node):
        _, name, index_expr = node
        info = self.symbols.lookup(name)
        print(">>> symbol lookup result:", info, type(info))
        if not info or info.kind != 'array':
            self.error(f"Access to undeclared or non-array variable '{name}'")
            return None
        
        index_type = self.visit(index_expr)
        if index_type != 'int':
            self.error(f"Array index must be of type 'int', got '{index_type}'")
    
        return info.type

    def visit_binop(self, node):
        _, op, left, right = node
        left_type = self.visit(left)
        right_type = self.visit(right)
        if left_type is None or right_type is None:
            return None
        if left_type != right_type:
            self.error(f"Type mismatch in binary operation '{op}': {left_type} vs {right_type}")
            return None
        return left_type

    def visit_unaryop(self, node):
        _, op, expr = node
        expr_type = self.visit(expr)
        if op == '!' and expr_type != 'int':
            self.error(f"Operator '!' expects 'int', got '{expr_type}'")
        elif op == '-' and expr_type not in ['int', 'float']:
            self.error(f"Unary '-' expects 'int' or 'float', got '{expr_type}'")
        return expr_type

    def visit_integer(self, node):
        return 'int'

    def visit_float(self, node):
        return 'float'

    def visit_char(self, node):
        return 'char'

    def visit_string(self, node):
        return 'string'

    def visit_variable(self, node):
        _, name = node
        info = self.symbols.lookup(name)
        if not info:
            self.error(f"Use of undeclared variable '{name}'")
            return None
        return info.type

    def visit_empty(self, node):
        return None
