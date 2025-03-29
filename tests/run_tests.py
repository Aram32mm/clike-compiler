import pytest

def main():
    # Run all tests in the tests/ folder
    exit_code = pytest.main(["tests"])
    # Optional: handle exit code
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")

if __name__ == "__main__":
    main()
