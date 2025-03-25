#!/usr/bin/env python3
import ply.lex as lex

class CLexer:
    # List of token names
    tokens = (
        'TYPE',
        'IDENTIFIER',
        'INTEGER',
        'PLUS',
        'MINUS',
        'MUL',
        'DIV',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'SEMICOLON',
        'ASSIGN',
        'RETURN',
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_SEMICOLON = r';'
    t_ASSIGN = r'='

    # Reserved words
    reserved = {
        'int': 'TYPE',
        'return': 'RETURN',
    }

    # Regular expression rules with actions
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # Test the lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)