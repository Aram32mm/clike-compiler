#!/usr/bin/env python3
"""
CLexer: Lexical analyzer for a C-like language.

This lexer is built using PLY (Python Lex-Yacc). It tokenizes input code written in a
C-like syntax and supports identifiers, keywords, arithmetic and logical operators,
grouping symbols, assignment, control flow keywords, comments, numeric literals,
string and character literals, as well as C-style constructs such as pointers,
arrays, and struct access.
"""

import ply.lex as lex

class CLexer:
    # === List of Token Names ===
    tokens = (
        'TYPE',         # int, float, etc.
        'IDENTIFIER',   # variable/function names
        'INTEGER',      # numeric literals
        'FLOAT',        # decimal numbers
        'CHAR',         # character literals
        'STRING',       # string literals
        'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
        'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE',
        'AND', 'OR', 'NOT',
        'ASSIGN',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
        'LBRACKET', 'RBRACKET', 'SEMICOLON', 'COMMA', 'DOT', 'ARROW', 'AMP',
        'IF', 'ELSE', 'WHILE', 'FOR', 'BREAK', 'CONTINUE', 'RETURN'
    )

    # === Regular Expression Rules for Simple Tokens ===
    t_PLUS       = r'\+'
    t_MINUS      = r'-'
    t_MUL        = r'\*'
    t_DIV        = r'/'
    t_MOD        = r'%'
    t_EQ         = r'=='
    t_NEQ        = r'!='
    t_GE         = r'>='
    t_LE         = r'<='
    t_GT         = r'>'
    t_LT         = r'<'
    t_AND        = r'&&'
    t_OR         = r'\|\|'
    t_NOT        = r'!'
    t_ASSIGN     = r'='
    t_LPAREN     = r'\('
    t_RPAREN     = r'\)'
    t_LBRACE     = r'\{'
    t_RBRACE     = r'\}'
    t_LBRACKET   = r'\['
    t_RBRACKET   = r'\]'
    t_SEMICOLON  = r';'
    t_COMMA      = r','
    t_DOT        = r'\.'
    t_ARROW      = r'->'
    t_AMP        = r'&'

    # === Reserved Keywords ===
    reserved = {
        'int': 'TYPE', 'float': 'TYPE', 'double': 'TYPE', 'char': 'TYPE', 'void': 'TYPE',
        'return': 'RETURN', 'if': 'IF', 'else': 'ELSE', 'while': 'WHILE',
        'for': 'FOR', 'break': 'BREAK', 'continue': 'CONTINUE'
    }

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_FLOAT(self, t):
        r'(\d+\.\d*|\.\d+)([eE][-+]?\d+)?'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CHAR(self, t):
        r"'(\\.|[^\\'])'"
        t.value = t.value[1:-1]
        return t

    def t_STRING(self, t):
        r'"([^\\\n]|(\\.))*?"'
        t.value = t.value[1:-1]
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r'//.*'
        pass

    def t_BLOCK_COMMENT(self, t):
        r'/\*[\s\S]*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass

    def t_PREPROCESSOR(self, t):
        r'\#[^\n]*'
        pass

    t_ignore = ' \t'

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        """
        Builds the lexer using PLY's lex() function.
        Call this before using tokenize() or test().
        """
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def tokenize(self, data):
        """
        Tokenizes the given input string and returns a list of (TYPE, value) tuples.
        Example:
            [('TYPE', 'int'), ('IDENTIFIER', 'x'), ('ASSIGN', '='), ('INTEGER', 5), ('SEMICOLON', ';')]
        """
        self.lexer.input(data)
        return [(tok.type, tok.value) for tok in iter(self.lexer.token, None)]

    def test(self, data, verbose=True):
        """
        Tests the lexer by printing all tokens found in the input string.
        Use for debugging or development.

        Args:
            data (str): Source code to lex.
            verbose (bool): If True, prints tokens.
        """
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            if verbose:
                print(tok)
