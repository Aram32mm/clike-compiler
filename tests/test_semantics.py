# tests/test_semantics.py

import pytest
from src.semantics import SemanticAnalyzer


@pytest.mark.parametrize("desc, ast", [
    (
        "basic assignment and return",
        [('FUNCTION', 'main', 'int', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 1)),
            ('ASSIGN', 'x', ('BINOP', '+', ('VARIABLE', 'x'), ('INTEGER', 2))),
            ('RETURN', ('VARIABLE', 'x'))
        ])]
    ),
    (
        "function with parameters and correct return",
        [('FUNCTION', 'sum', 'int', [('PARAM', 'int', 'a'), ('PARAM', 'int', 'b')], [
            ('VAR_DECL_INIT', 'int', 'result', ('BINOP', '+', ('VARIABLE', 'a'), ('VARIABLE', 'b'))),
            ('RETURN', ('VARIABLE', 'result'))
        ])]
    ),
    (
        "array declaration and access",
        [('FUNCTION', 'main', 'void', [], [
            ('ARRAY_DECL', 'int', 'arr', ('INTEGER', 10)),
            ('VAR_DECL_INIT', 'int', 'i', ('INTEGER', 0)),
            ('VAR_DECL_INIT', 'int', 'x', ('ARRAY_ACCESS', 'arr', ('VARIABLE', 'i')))
        ])]
    ),
    (
        "nested block scopes with shadowing",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 1)),
            ('BLOCK', [
                ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 2)),
                ('ASSIGN', 'x', ('INTEGER', 3))
            ]),
            ('ASSIGN', 'x', ('INTEGER', 4))
        ])]
    ),
    (
        "void function with return",
        [('FUNCTION', 'main', 'void', [], [
            ('RETURN', None)
        ])]
    ),
    (
        "unary operation on integer",
        [('FUNCTION', 'main', 'int', [], [
            ('RETURN', ('UNARYOP', '-', ('INTEGER', 5)))
        ])]
    ),
    (
        "call to user-defined function",
        [
            ('FUNCTION', 'main', 'int', [], [
                ('RETURN', ('CALL', 'square', [('INTEGER', 4)]))
            ]),
            ('FUNCTION', 'square', 'int', [('PARAM', 'int', 'n')], [
                ('RETURN', ('BINOP', '*', ('VARIABLE', 'n'), ('VARIABLE', 'n')))
            ])
        ]
    ),
])
def test_valid_semantics(desc, ast):
    analyzer = SemanticAnalyzer(verbose=False)
    errors = analyzer.analyze(ast)
    assert errors == [], f"{desc} failed:\nExpected no errors, but got: {errors}"


@pytest.mark.parametrize("desc, ast, expected_errors", [
    (
        "valid program",
        [('FUNCTION', 'main', 'int', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 1)),
            ('ASSIGN', 'x', ('BINOP', '+', ('VARIABLE', 'x'), ('INTEGER', 2))),
            ('RETURN', ('VARIABLE', 'x'))
        ])],
        []
    ),
    (
        "undeclared variable",
        [('FUNCTION', 'main', 'void', [], [
            ('ASSIGN', 'x', ('INTEGER', 5)),
        ])],
        ["Assignment to undeclared variable 'x'"]
    ),
    (
        "redeclaration",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL', 'int', 'x'),
            ('VAR_DECL', 'int', 'x'),
        ])],
        ["Variable 'x' already declared"]
    ),
    (
        "undeclared function call",
        [('FUNCTION', 'main', 'void', [], [
            ('CALL', 'foo', [('INTEGER', 1)]),
        ])],
        ["Call to undeclared function 'foo'"]
    ),
    (
        "undeclared array access",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'i', ('INTEGER', 0)),
            ('ARRAY_ACCESS', 'arr', ('VARIABLE', 'i')),
        ])],
        ["Access to undeclared or non-array variable 'arr'"]
    ),
    (
        "use of undeclared variable in expression",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('VARIABLE', 'y')),
        ])],
        ["Use of undeclared variable 'y'"]
    ),
    (
        "type mismatch in assignment",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 1)),
            ('ASSIGN', 'x', ('STRING', 'hello')),
        ])],
        ["Type mismatch in assignment to 'x': int = string"]
    ),
    (
        "type mismatch in declaration",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('STRING', 'oops')),
        ])],
        ["Type mismatch in declaration: int x = string"]
    ),
    (
        "type mismatch in binary operation",
        [('FUNCTION', 'main', 'void', [], [
            ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 2)),
            ('VAR_DECL_INIT', 'string', 's', ('STRING', 'hi')),
            ('VAR_DECL_INIT', 'int', 'z', ('BINOP', '+', ('VARIABLE', 'x'), ('VARIABLE', 's')))
        ])],
        ["Type mismatch in binary operation '+': int vs string"]
    ),
    (
        "function call with too few args",
        [
            ('FUNCTION', 'main', 'void', [], [
                ('CALL', 'sum', [('INTEGER', 1)])
            ]),
            ('FUNCTION', 'sum', 'int', [('PARAM', 'int', 'a'), ('PARAM', 'int', 'b')], [
                ('RETURN', ('BINOP', '+', ('VARIABLE', 'a'), ('VARIABLE', 'b')))
            ])
        ],
        ["Function 'sum' called with wrong number of arguments: expected 2, got 1"]
    ),
    (
        "function call with wrong arg types",
        [
            ('FUNCTION', 'main', 'void', [], [
                ('CALL', 'sum', [('INTEGER', 1), ('STRING', 'no')])
            ]),
            ('FUNCTION', 'sum', 'int', [('PARAM', 'int', 'a'), ('PARAM', 'int', 'b')], [
                ('RETURN', ('BINOP', '+', ('VARIABLE', 'a'), ('VARIABLE', 'b')))
            ])
        ],
        ["Type mismatch in argument 2 of call to 'sum': expected int, got string"]
    ),
    (
        "return type mismatch",
        [('FUNCTION', 'main',  'int', [], [
            ('RETURN', ('STRING', 'oops'))
        ])],
        ["Return type mismatch: expected int, got string"] 
    ),
])
def test_invalid_semantics(desc, ast, expected_errors):
    analyzer = SemanticAnalyzer(verbose=False)
    errors = analyzer.analyze(ast)
    assert errors == expected_errors, f"{desc} failed:\nExpected: {expected_errors}\nGot: {errors}"
