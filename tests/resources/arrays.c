/* Test for arrays */

int main() {
    // Array declaration and initialization
    int numbers[5];
    int initialized[3] = {10, 20, 30};
    int result = 0;
    
    // Array element assignment
    numbers[0] = 5;
    numbers[1] = 10;
    numbers[2] = 15;
    numbers[3] = 20;
    numbers[4] = 25;
    
    // Array element access
    result = result + numbers[2];
    result = result + initialized[1];
    
    // Array iteration
    int i;
    for (i = 0; i < 5; i = i + 1) {
        result = result + numbers[i];
    }
    
    // Using array elements in expressions
    int sum = numbers[0] + numbers[1] + numbers[2];
    result = result + sum;
    
    // Array as function parameter
    // Note: If your compiler doesn't support passing arrays to functions,
    // this part can be adjusted or removed
    
    // Nested arrays
    int matrix[2][2];
    matrix[0][0] = 1;
    matrix[0][1] = 2;
    matrix[1][0] = 3;
    matrix[1][1] = 4;
    
    result = result + matrix[0][0] + matrix[1][1];
    
    return result;
}