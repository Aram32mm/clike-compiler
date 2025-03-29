# tests/test_codegen.py

import pytest
from src.codegen import CodeGenerator  # adjust the import path if needed

@pytest.fixture
def codegen():
    return CodeGenerator(verbose=True)

def test_simple_assignment(codegen):
    ast = ('FUNCTION', 'main', [], [
        ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 5)),
        ('ASSIGN', 'x', ('BINOP', '+', ('VARIABLE', 'x'), ('INTEGER', 2))),
        ('RETURN', ('VARIABLE', 'x'))
    ])
    output = codegen.generate(ast)
    print(output)
    assert "LOADC 5" in output
    assert "ADD" in output
    assert "RETURN" in output


def test_if_else_codegen(codegen):
    ast = ('FUNCTION', 'main', [], [
        ('VAR_DECL_INIT', 'int', 'x', ('INTEGER', 10)),
        ('IF_ELSE', ('BINOP', '>', ('VARIABLE', 'x'), ('INTEGER', 0)),
            ('ASSIGN', 'x', ('INTEGER', 1)),
            ('ASSIGN', 'x', ('INTEGER', -1))),
        ('RETURN', ('VARIABLE', 'x'))
    ])
    output = codegen.generate(ast)
    print(output)
    assert "GE" in output  # '>' is mapped to GE
    assert "JUMPZ" in output
    assert "JUMP" in output
    assert "STOREA" in output


def test_while_codegen(codegen):
    ast = ('FUNCTION', 'main', [], [
        ('VAR_DECL_INIT', 'int', 'i', ('INTEGER', 0)),
        ('WHILE', ('BINOP', '<', ('VARIABLE', 'i'), ('INTEGER', 3)),
            ('ASSIGN', 'i', ('BINOP', '+', ('VARIABLE', 'i'), ('INTEGER', 1)))),
        ('RETURN', ('VARIABLE', 'i'))
    ])
    output = codegen.generate(ast)
    print(output)
    assert "LE" in output  # '<' is mapped to LE
    assert "JUMPZ" in output
    assert "JUMP" in output

