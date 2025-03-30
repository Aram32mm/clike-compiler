# tests/test_lexer.py
 
import pytest
from src.lexer import CLexer


@pytest.fixture
def lexer():
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


def test_float_and_integer_literals(lexer):
    code = "float x = 3.14; int y = 42;"
    tokens = lexer.tokenize(code)
    assert tokens == [
        ('TYPE', 'float'),
        ('IDENTIFIER', 'x'),
        ('ASSIGN', '='),
        ('FLOAT', 3.14),
        ('SEMICOLON', ';'),
        ('TYPE', 'int'),
        ('IDENTIFIER', 'y'),
        ('ASSIGN', '='),
        ('INTEGER', 42),
        ('SEMICOLON', ';'),
    ]


def test_operators_and_grouping(lexer):
    code = "(a + b) * c / d - e % f;"
    tokens = lexer.tokenize(code)
    expected = [
        ('LPAREN', '('),
        ('IDENTIFIER', 'a'),
        ('PLUS', '+'),
        ('IDENTIFIER', 'b'),
        ('RPAREN', ')'),
        ('MUL', '*'),
        ('IDENTIFIER', 'c'),
        ('DIV', '/'),
        ('IDENTIFIER', 'd'),
        ('MINUS', '-'),
        ('IDENTIFIER', 'e'),
        ('MOD', '%'),
        ('IDENTIFIER', 'f'),
        ('SEMICOLON', ';'),
    ]
    assert tokens == expected


def test_comparison_and_logical_operators(lexer):
    code = "if (a >= b && c != d || !e) {}"
    tokens = lexer.tokenize(code)
    expected = [
        ('IF', 'if'),
        ('LPAREN', '('),
        ('IDENTIFIER', 'a'),
        ('GE', '>='),
        ('IDENTIFIER', 'b'),
        ('AND', '&&'),
        ('IDENTIFIER', 'c'),
        ('NEQ', '!='),
        ('IDENTIFIER', 'd'),
        ('OR', '||'),
        ('NOT', '!'),
        ('IDENTIFIER', 'e'),
        ('RPAREN', ')'),
        ('LBRACE', '{'),
        ('RBRACE', '}'),
    ]
    assert tokens == expected


def test_char_and_string_literals(lexer):
    code = "char c = 'x'; char* s = \"hello\\nworld\";"
    tokens = lexer.tokenize(code)
    expected = [
        ('TYPE', 'char'),
        ('IDENTIFIER', 'c'),
        ('ASSIGN', '='),
        ('CHAR', 'x'),
        ('SEMICOLON', ';'),
        ('TYPE', 'char'),
        ('MUL', '*'),
        ('IDENTIFIER', 's'),
        ('ASSIGN', '='),
        ('STRING', 'hello\\nworld'),
        ('SEMICOLON', ';'),
    ]
    assert tokens == expected


def test_struct_access_and_pointers(lexer):
    code = "node->next = &head;"
    tokens = lexer.tokenize(code)
    expected = [
        ('IDENTIFIER', 'node'),
        ('ARROW', '->'),
        ('IDENTIFIER', 'next'),
        ('ASSIGN', '='),
        ('AMP', '&'),
        ('IDENTIFIER', 'head'),
        ('SEMICOLON', ';'),
    ]
    assert tokens == expected


def test_array_access(lexer):
    code = "arr[0] = data[i];"
    tokens = lexer.tokenize(code)
    expected = [
        ('IDENTIFIER', 'arr'),
        ('LBRACKET', '['),
        ('INTEGER', 0),
        ('RBRACKET', ']'),
        ('ASSIGN', '='),
        ('IDENTIFIER', 'data'),
        ('LBRACKET', '['),
        ('IDENTIFIER', 'i'),
        ('RBRACKET', ']'),
        ('SEMICOLON', ';'),
    ]
    assert tokens == expected


def test_control_flow_keywords(lexer):
    code = "for (;;) { continue; break; return; }"
    tokens = lexer.tokenize(code)
    expected = [
        ('FOR', 'for'),
        ('LPAREN', '('),
        ('SEMICOLON', ';'),
        ('SEMICOLON', ';'),
        ('RPAREN', ')'),
        ('LBRACE', '{'),
        ('CONTINUE', 'continue'),
        ('SEMICOLON', ';'),
        ('BREAK', 'break'),
        ('SEMICOLON', ';'),
        ('RETURN', 'return'),
        ('SEMICOLON', ';'),
        ('RBRACE', '}'),
    ]
    assert tokens == expected


def test_comments_and_preprocessor_are_ignored(lexer):
    code = (
        "#include <stdio.h>\n"
        "// This is a single-line comment\n"
        "/* This is a \n"
        "   block comment */\n"
        "int x = 10; // Inline comment\n"
    )
    tokens = lexer.tokenize(code)
    expected = [
        ('TYPE', 'int'),
        ('IDENTIFIER', 'x'),
        ('ASSIGN', '='),
        ('INTEGER', 10),
        ('SEMICOLON', ';'),
    ]
    assert tokens == expected


def test_illegal_character(lexer):
    code = "int €uro = 1;"
    with pytest.raises(SyntaxError, match=r"Illegal character '€'"):
        lexer.tokenize(code)
