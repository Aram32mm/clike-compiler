"""
Symbol Table implementation for the C-like compiler.
Tracks identifiers and their attributes throughout different scopes.
"""


class Symbol:
    """Represents a single symbol (variable, function) in the program."""
    
    def __init__(self, name, type_, is_function=False, params=None, line_num=None):
        """
        Initialize a symbol.
        
        Args:
            name (str): The identifier name
            type_ (str): The data type (e.g., 'int')
            is_function (bool): Whether this is a function
            params (list): If a function, the parameter types
            line_num (int): Line number where defined
        """
        self.name = name
        self.type = type_
        self.is_function = is_function
        self.params = params if params else []
        self.line_num = line_num
        self.address = None  # Will be assigned during code generation
    
    def __repr__(self):
        if self.is_function:
            return f"Function {self.name}: {self.type} {self.params}"
        return f"Variable {self.name}: {self.type}"


class Scope:
    """Represents a single scope in the program."""
    
    def __init__(self, parent=None):
        """
        Initialize a scope.
        
        Args:
            parent (Scope): Parent scope, if any
        """
        self.symbols = {}  # Maps names to Symbol objects
        self.parent = parent
        self.children = []
        
    def add_symbol(self, symbol):
        """
        Add a symbol to the current scope.
        
        Args:
            symbol (Symbol): The symbol to add
            
        Returns:
            bool: True if added successfully, False if name already exists in this scope
        """
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup(self, name):
        """
        Look up a symbol in this scope.
        
        Args:
            name (str): The name to look up
            
        Returns:
            Symbol or None: The symbol if found, otherwise None
        """
        return self.symbols.get(name)
    
    def create_child_scope(self):
        """
        Create a new child scope.
        
        Returns:
            Scope: The new child scope
        """
        child = Scope(parent=self)
        self.children.append(child)
        return child


class SymbolTable:
    """Manages symbols across multiple scopes."""
    
    def __init__(self):
        """Initialize the symbol table with a global scope."""
        self.current_scope = Scope()  # Start with global scope
        self.global_scope = self.current_scope
        
    def enter_scope(self):
        """
        Enter a new scope.
        
        Returns:
            Scope: The new current scope
        """
        self.current_scope = self.current_scope.create_child_scope()
        return self.current_scope
    
    def exit_scope(self):
        """
        Exit the current scope.
        
        Returns:
            Scope: The new current scope (parent)
            
        Raises:
            Exception: If trying to exit the global scope
        """
        if self.current_scope.parent is None:
            raise Exception("Cannot exit global scope")
        self.current_scope = self.current_scope.parent
        return self.current_scope
    
    def add_symbol(self, symbol):
        """
        Add a symbol to the current scope.
        
        Args:
            symbol (Symbol): The symbol to add
            
        Returns:
            bool: True if added successfully
            
        Raises:
            Exception: If the symbol name already exists in the current scope
        """
        if not self.current_scope.add_symbol(symbol):
            raise Exception(f"Symbol '{symbol.name}' already defined in this scope")
        return True
    
    def lookup(self, name, current_scope_only=False):
        """
        Look up a symbol in all accessible scopes.
        
        Args:
            name (str): The name to look up
            current_scope_only (bool): If True, only look in the current scope
            
        Returns:
            Symbol or None: The symbol if found, otherwise None
        """
        symbol = self.current_scope.lookup(name)
        if symbol or current_scope_only:
            return symbol
        
        # If not found and not limited to current scope, check parent scopes
        scope = self.current_scope.parent
        while scope:
            symbol = scope.lookup(name)
            if symbol:
                return symbol
            scope = scope.parent
        
        return None


# Example usage:
# from symbol_table import SymbolTable, Symbol
# 
# # Create a symbol table
# sym_table = SymbolTable()
# 
# # Add a variable in global scope
# sym_table.add_symbol(Symbol("x", "int", line_num=5))
# 
# # Enter a new scope (e.g., a function)
# sym_table.enter_scope()
# 
# # Add a local variable
# sym_table.add_symbol(Symbol("y", "int", line_num=7))
# 
# # Look up variables
# x = sym_table.lookup("x")  # Found in parent scope
# y = sym_table.lookup("y")  # Found in current scope
# z = sym_table.lookup("z")  # Not found
# 
# # Exit the scope
# sym_table.exit_scope()