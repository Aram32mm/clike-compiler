# tests/integration.py

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.utils.runner import compare_results
from compiler import compile_file

resource_dir = "./tests/resources"

test_files = [
    os.path.join(resource_dir, f)
    for f in os.listdir(resource_dir)
    if f.endswith(".c")
]

@pytest.mark.parametrize("c_file_path", test_files)
def test_integration(c_file_path):
    print(f"\n🧪 Testing: {c_file_path}")
    cma_path = c_file_path.replace(".c", ".cma")

    # Step 1: Compile C-like to CMA
    success = compile_file(c_file_path, verbose=True)
    assert success, f"❌ Compilation to CMA failed for {c_file_path}"

    # Step 2: Compare native C vs CMA
    match = compare_results(c_file_path, cma_path, verbose=True)   
    
    # Step 3: Enforce correctness
    assert match, f"❌ Test failed: {c_file_path} (C != CMA)"
    
    # Cleanup only if test passed
    if os.path.exists(cma_path):
        os.remove(cma_path)

# === Allow single-file execution ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tests/integration.py <source.c>")
        sys.exit(1)

    c_file_path = sys.argv[1]
    if not os.path.isfile(c_file_path):
        print(f"❌ File not found: {c_file_path}")
        sys.exit(1)

    print(f"\n🧪 Debug Testing: {c_file_path}")
    cma_path = c_file_path.replace(".c", ".cma")

    success = compile_file(c_file_path, verbose=True)
    if not success:
        print(f"❌ Compilation failed: {c_file_path}")
        sys.exit(1)

    match = compare_results(c_file_path, cma_path, verbose=True)
    if not match:
        print(f"❌ Mismatch: {c_file_path}")
        sys.exit(1)

    print("✅ Test passed.")

    if os.path.exists(cma_path):
        os.remove(cma_path)
