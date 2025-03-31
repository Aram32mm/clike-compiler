import os
import sys
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tests.utils.cma_parser import CMaProgramParser
from tests.utils.cma_instruction import CMaInstructionProcessor

"""
Note: The returncode returns the value as the program's exit code, 
which typically should be between 0-255. 

Any number outside this range is undefined (will wrap around)
All test output should be < 255
"""
def compile_and_run_c_program(c_file_path):
    # Get filename without extension
    base_name = os.path.splitext(os.path.basename(c_file_path))[0]
    output_exe = f"{base_name}.out"

    # Compile the C file
    compile_process = subprocess.run(
        ["gcc", c_file_path, "-o", output_exe],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if compile_process.returncode != 0:
        print(f"❌ Compilation failed for {c_file_path}:\n{compile_process.stderr}")
        return None

    # Run the executable
    run_process = subprocess.run(
        [f"./{output_exe}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Clean up
    os.remove(output_exe)

    return run_process.returncode  # Value returned from main()

def run_cma_program(cma_file_path):
    with open(cma_file_path, "r") as f:
        raw_program = f.read()

    parser = CMaProgramParser()
    instructions = parser.parse_string(raw_program)

    vm = CMaInstructionProcessor(verbose=True)
    vm.load_instructions(instructions)
    vm.run()

    return vm.return_value

def compare_results(c_file_path, cma_file_path, verbose=False):
    if verbose:
        print(f"\n🔍 Comparing: {c_file_path} && {cma_file_path}")

    # Step 1: Compile and run C
    c_result = compile_and_run_c_program(c_file_path)
    if verbose:
        print(f"🔹 Native C result: {c_result}")

    # Step 2: Process CMA instructions given
    cma_result = run_cma_program(cma_file_path)
    if verbose:
        print(f"🔸 CMA VM result: {cma_result}")

    # Step 3: Compare results
    if c_result == cma_result:
        if verbose:
            print("✅ Match!")
        return True
    else:
        if verbose:
            print("❌ Mismatch!")
        return False