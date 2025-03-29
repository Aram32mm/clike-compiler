# tests/integration.py

from tests.utils.cma_parser import CMaProgramParser
from tests.utils.cma_instruction import CMaInstructionProcessor

def test_integration():
    """
    TODO: Weram
    The idea is to compile all c files in resources (our test cases) 
    with both our compiler and a c compiler 

    out compiler produces the cma instructions, so once you have those instructions, 
    use the parser and the processor to get the result

    at the end you shpuld compare the result given by our compiler and the processor
    with the result given by a compilation of the c code with gcc or something similar
    look how to automatize that process
    

    """
    raw_program = """
    LOADC 3    // Push 3 onto the stack
    LOADC 4    // Push 4 onto the stack
    ADD        // Add 3 and 4, result is 7
    LOADC 4    // Push 4 onto the stack
    NEG        // Negate 4, result is -4
    DIV        // Divide 7 by -4, result is -1.75
    """

    #parser = CMaProgramParser()
    #instructions = parser.parse_string(raw_program)

    #vm = CMaInstructionProcessor(verbose=True)
    #vm.load_instructions(instructions)
    #vm.run()
    assert 1 == 1
