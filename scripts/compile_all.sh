#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p ./test_output

# Compile each example file
echo "Compiling example input files..."

for file in ./example_input/*.c; do
    filename=$(basename "$file" .c)
    output_file="./test_output/${filename}.cma"
    
    echo "Compiling $file to $output_file"
    python3 compiler.py "$file" -o "$output_file"
    
    # Check if compilation was successful
    if [ $? -eq 0 ]; then
        echo "✅ Successfully compiled $filename"
        echo "Output:"
        cat "$output_file"
        echo ""
    else
        echo "❌ Failed to compile $filename"
        echo ""
    fi
done

echo "Compilation complete!"