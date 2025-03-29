#!/usr/bin/env python3
"""Symbol table module for storing variable and function metadata."""


class SymbolInfo:
    """Holds metadata about a declared symbol (variable, function, etc.)."""

    def __init__(self, name, symbol_type, kind, extra=None):
        self.name = name  # variable or function name
        self.type = symbol_type  # e.g., 'int', 'int[]', 'function'
        self.kind = kind  # 'var', 'param', 'array', 'func'
        self.extra = extra or {}  # additional info (e.g., array size, param list)

    def __repr__(self):
        return f"<{self.kind} {self.name}: {self.type} {self.extra}>"


class SymbolTable:
    """Represents a scoped symbol table for managing identifiers."""

    def __init__(self):
        self.scopes = [{}]  # Stack of dictionaries representing nested scopes

    def push_scope(self):
        """Push a new scope level (e.g., entering a block)."""
        self.scopes.append({})

    def pop_scope(self):
        """Pop the current scope level (e.g., exiting a block)."""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot pop the global scope.")

    def declare(self, name, symbol_type, kind, extra=None):
        """Declare a new symbol in the current scope."""
        if name in self.scopes[-1]:
            raise Exception(f"Redeclaration of '{name}' in the current scope.")
        self.scopes[-1][name] = SymbolInfo(name, symbol_type, kind, extra)

    def lookup(self, name):
        """Look up a symbol by name in the current or enclosing scopes."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def __repr__(self):
        return '\n'.join([f"Scope {i}: {scope}" for i, scope in enumerate(self.scopes)])
