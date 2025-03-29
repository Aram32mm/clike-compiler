# tests/test_parser.py

from src.parser import CParser

def test_parser_basic():
    source_code = """
    int add(int a, int b) {
        int result = a + b;
        return result;
    }

    int main() {
        int x = 5;
        int y = 3;
        int z = add(x, y);
        return 0;
    }
    """
    parser = CParser(verbose=True)
    result = parser.parse(source_code)
    assert result is not None
    assert result[0][0] == 'FUNCTION'  # First function
    assert result[0][1] == 'add'
    assert result[1][0] == 'FUNCTION'  # Second function
    assert result[1][1] == 'main'

