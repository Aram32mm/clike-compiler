#!/usr/bin/env python3
"""
C-like Language Compiler

This script compiles a simplified C-like language to CMA code.
"""

import sys
import os
import argparse
from src.lexer import CLexer
from src.parser import CParser
from src.codegen import CodeGenerator

def compile_file(input_file, output_file=None):
    """Compile the input file to CMA code and write to the output file"""
    try:
        # Read the input file
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        # If no output file is specified, use the input filename with .cma extension
        if output_file is None:
            output_file = os.path.splitext(input_file)[0] + '.cma'
        
        # Parse the source code
        parser = CParser()
        ast = parser.parse(source_code)
        
        if ast is None:
            print("Parsing failed.")
            return False
        
        import pprint
        pprint.pprint(ast)
        
        # Generate code
        code_generator = CodeGenerator()
        cma_code = code_generator.generate(ast)
        
        # Write the output
        with open(output_file, 'w') as f:
            f.write(cma_code)
        
        print(f"Compilation successful. Output written to {output_file}")
        return True
    
    except FileNotFoundError:
        print(f"Error: Could not open input file {input_file}")
        return False
    except Exception as e:
        print(f"Compilation error: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Compile C-like language to CMA code')
    parser.add_argument('input_file', help='The C-like source file to compile')
    parser.add_argument('-o', '--output', help='Output file name (default: input file with .cma extension)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    success = compile_file(args.input_file, args.output)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()