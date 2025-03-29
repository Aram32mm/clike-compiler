import pytest
from src.semantics import SemanticAnalyzer

@pytest.fixture
def analyzer():
    return SemanticAnalyzer(verbose=True)

def test_valid_program(analyzer):
    ast = [('FUNCTION', 'main', [], [
        ('VAR_DECL', 'int', 'x'),
        ('ASSIGN', 'x', ('INTEGER', 42)),
        ('RETURN', ('VARIABLE', 'x'))
    ])]
    errors = analyzer.analyze(ast)
    assert errors == []

def test_undeclared_variable(analyzer):
    ast = [('FUNCTION', 'main', [], [
        ('ASSIGN', 'x', ('INTEGER', 1)),
        ('RETURN', ('VARIABLE', 'x'))
    ])]
    errors = analyzer.analyze(ast)
    assert any("undeclared variable 'x'" in e for e in errors)

def test_redeclaration(analyzer):
    ast = [('FUNCTION', 'main', [], [
        ('VAR_DECL', 'int', 'x'),
        ('VAR_DECL', 'int', 'x')
    ])]
    errors = analyzer.analyze(ast)
    assert any("already declared" in e for e in errors)

def test_function_call_undeclared(analyzer):
    ast = [('FUNCTION', 'main', [], [
        ('CALL', 'foo', [('INTEGER', 1)])
    ])]
    errors = analyzer.analyze(ast)
    assert any("undeclared function 'foo'" in e for e in errors)

def test_array_access_undeclared(analyzer):
    ast = [('FUNCTION', 'main', [], [
        ('ARRAY_ACCESS', 'arr', ('INTEGER', 0))
    ])]
    errors = analyzer.analyze(ast)
    assert any("undeclared array 'arr'" in e for e in errors)
