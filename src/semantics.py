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

    def analyze(self, ast):
        if isinstance(ast, list):
            for node in ast:
                self.visit(node)
        else:
            self.visit(ast)
        return self.errors

    def error(self, message):
        self.errors.append(message)
        if self.verbose:
            print(f"❌ Semantic error: {message}")

    def visit(self, node):
        kind = node[0]
        method = getattr(self, f"visit_{kind.lower()}", None)
        if method:
            method(node)
        else:
            self.error(f"No handler for AST node {kind}")

    def visit_function(self, node):
        _, name, params, body = node
        self.symbols.push_scope()
        for _, t, n in params:
            self.symbols.declare(n, t, 'param')
        for stmt in body:
            self.visit(stmt)
        self.symbols.pop_scope()

    def visit_var_decl(self, node):
        _, t, name = node
        if self.symbols.lookup(name):
            self.error(f"Variable '{name}' already declared")
        else:
            self.symbols.declare(name, t, 'var')

    def visit_var_decl_init(self, node):
        _, t, name, expr = node
        if self.symbols.lookup(name):
            self.error(f"Variable '{name}' already declared")
        else:
            self.symbols.declare(name, t, 'var')
        self.visit(expr)

    def visit_array_decl(self, node):
        _, t, name, size_expr = node
        if self.symbols.lookup(name):
            self.error(f"Array '{name}' already declared")
        else:
            self.symbols.declare(name, t, 'array')
        self.visit(size_expr)

    def visit_assign(self, node):
        _, name, expr = node
        if not self.symbols.lookup(name):
            self.error(f"Assignment to undeclared variable '{name}'")
        self.visit(expr)

    def visit_return(self, node):
        _, expr = node
        if expr is not None:
            self.visit(expr)

    def visit_if(self, node):
        _, cond, then = node
        self.visit(cond)
        self.visit(then)

    def visit_if_else(self, node):
        _, cond, then, otherwise = node
        self.visit(cond)
        self.visit(then)
        self.visit(otherwise)

    def visit_while(self, node):
        _, cond, body = node
        self.visit(cond)
        self.visit(body)

    def visit_for(self, node):
        _, init, cond, update, body = node
        self.symbols.push_scope()
        self.visit(init)
        self.visit(cond)
        self.visit(update)
        self.visit(body)
        self.symbols.pop_scope()

    def visit_block(self, node):
        _, stmts = node
        self.symbols.push_scope()
        for stmt in stmts:
            self.visit(stmt)
        self.symbols.pop_scope()

    def visit_call(self, node):
        _, func_name, args = node
        if not self.symbols.lookup(func_name):
            self.error(f"Call to undeclared function '{func_name}'")
        for arg in args:
            self.visit(arg)

    def visit_array_access(self, node):
        _, name, index_expr = node
        if not self.symbols.lookup(name):
            self.error(f"Access to undeclared array '{name}'")
        self.visit(index_expr)

    def visit_binop(self, node):
        _, op, left, right = node
        self.visit(left)
        self.visit(right)

    def visit_unaryop(self, node):
        _, op, expr = node
        self.visit(expr)

    def visit_integer(self, node):
        pass

    def visit_float(self, node):
        pass

    def visit_char(self, node):
        pass

    def visit_string(self, node):
        pass

    def visit_variable(self, node):
        _, name = node
        if not self.symbols.lookup(name):
            self.error(f"Use of undeclared variable '{name}'")

    def visit_empty(self, node):
        pass
