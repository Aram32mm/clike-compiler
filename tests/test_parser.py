# tests/test_parser.py

import pytest
from src.parser import CParser


@pytest.fixture(scope="module")
def parser():
    return CParser(verbose=True)


@pytest.mark.parametrize("code,expected", [
    # FUNCTION (empty)
    ("void main() {}", [
        ('FUNCTION', 'main', 'void', [], [])
    ]),

    # FUNCTION with params and return
    ("int add(int a, int b) { return a + b; }", [
        ('FUNCTION', 'add', 'int', 
         [('PARAM', 'int', 'a'), ('PARAM', 'int', 'b')],
         [('RETURN', ('BINOP', '+', ('VARIABLE', 'a'), ('VARIABLE', 'b')))])
    ]),

    # VAR_DECL, VAR_DECL_INIT, ARRAY_DECL
    ("void main() { int x; float y = 2.5; char str[10]; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL', 'int', 'x'),
            ('VAR_DECL_INIT', 'float', 'y', ('FLOAT', 2.5)),
            ('ARRAY_DECL', 'char', 'str', 10)
        ])
    ]),

    # ASSIGN, ARRAY_ASSIGN
    ("void main() { x = 1; a[0] = 2; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('ASSIGN', 'x', ('INTEGER', 1)),
            ('ARRAY_ASSIGN', 'a', ('INTEGER', 0), ('INTEGER', 2))
        ])
    ]),

    # IF + IF_ELSE
    ("void main() { if (x) x = 1; else x = 2; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('IF_ELSE', ('VARIABLE', 'x'),
             ('ASSIGN', 'x', ('INTEGER', 1)),
             ('ASSIGN', 'x', ('INTEGER', 2)))
        ])
    ]),

    # WHILE
    ("void main() { while (x < 5) x = x + 1; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('WHILE', ('BINOP', '<', ('VARIABLE', 'x'), ('INTEGER', 5)),
             ('ASSIGN', 'x', ('BINOP', '+', ('VARIABLE', 'x'), ('INTEGER', 1))))
        ])
    ]),

    # FOR with expressions
    ("void main() { for (x = 0; x < 3; x = x + 1) x = x * 2; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('FOR',
             ('ASSIGN', 'x', ('INTEGER', 0)),
             ('BINOP', '<', ('VARIABLE', 'x'), ('INTEGER', 3)),
             ('ASSIGN', 'x', ('BINOP', '+', ('VARIABLE', 'x'), ('INTEGER', 1))),
             ('ASSIGN', 'x', ('BINOP', '*', ('VARIABLE', 'x'), ('INTEGER', 2))))
        ])
    ]),

    # RETURN and RETURN void
    ("int main() { return 42; }", [
        ('FUNCTION', 'main', 'int', [], [('RETURN', ('INTEGER', 42))])
    ]),
    ("void main() { return; }", [
        ('FUNCTION', 'main', 'void', [], [('RETURN', None)])
    ]),

    # BLOCK and nested BLOCK
    ("void main() { { int x = 5; } }", [
        ('FUNCTION', 'main', 'void', [], [
            ('BLOCK', [('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 5))])
        ])
    ]),

    # FUNCTION CALL
    ("void main() { int r = f(1, 2); }", [
        ('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'r',
             ('CALL', 'f', [('INTEGER', 1), ('INTEGER', 2)]))
        ])
    ]),

    # ARRAY_ACCESS
    ("void main() { int a = arr[3]; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'a', ('ARRAY_ACCESS', 'arr', ('INTEGER', 3)))
        ])
    ]),

    # UNARYOP + grouping
    ("void main() { int x = -(1 + 2); }", [
        ('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x',
             ('UNARYOP', '-', ('BINOP', '+', ('INTEGER', 1), ('INTEGER', 2))))
        ])
    ]),

    # STRING + CHAR literals
    ("void main() { char c = 'a'; char* s = \"hi\"; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'char', 'c', ('CHAR', 'a')),
            ('VAR_DECL_INIT', 'char*', 's', ('STRING', 'hi'))
        ])
    ]),

    # BREAK + CONTINUE
    ("void main() { break; continue; }", [
        ('FUNCTION', 'main', 'void', [], [
            ('BREAK',),
            ('CONTINUE',)
        ])
    ]),
])
def test_parser_ast(parser, code, expected):
    result = parser.parse(code)
    assert result == expected, f"\nExpected:\n{expected}\n\nGot:\n{result}"


@pytest.mark.parametrize("code", [

    # Missing semicolon
    "void main() { int x = 5 }",

    # Incomplete function
    "int add(int a, int b)",

    # Unmatched parentheses
    "void main() { if (x > 0) (x = 1; }",

    # Invalid assignment target
    "void main() { 3 = x; }",

    # Array declaration without size
    "void main() { int arr[]; }",

    # Missing type
    "main() { return 0; }",

    # Function call missing closing paren
    "void main() { f(1, 2; }",

    # Invalid character
    "void main() { int €uro = 1; }",

    # Invalid operator
    "void main() { x ** y; }",

    # For loop with missing parts
    "void main() { for (; x < 5) x = 1; }",

])
def test_invalid_inputs_raise_syntax_error(parser, code):
    with pytest.raises(SyntaxError, match=r"Syntax error|Illegal character"):
        parser.parse(code)
