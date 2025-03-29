# tests/test_lexer.py

import pytest
from src.lexer import CLexer

@pytest.fixture
def lexer():
    """Build and return a fresh lexer instance for each test"""
    lexer = CLexer()
    lexer.build()
    return lexer

def test_simple_declaration(lexer):
    code = "int a = 5;"
    tokens = lexer.tokenize(code)
    assert tokens == [
        ('TYPE', 'int'),
        ('IDENTIFIER', 'a'),
        ('ASSIGN', '='),
        ('INTEGER', 5),
        ('SEMICOLON', ';'),
    ]
