/* Test for functions */

// Function declarations
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Function with multiple parameters
int calculate(int a, int b, int c) {
    return a * b + c;
}

// Function with no parameters
int getConstant() {
    return 42;
}

// Void function
void updateValue(int a) {
    a = a + 10;
    // No return needed
}

// Main function
int main() {
    int result = 0;
    
    // Simple function calls
    result = result + add(5, 3);
    result = result + subtract(10, 4);
    result = result + multiply(3, 7);
    
    // Nested function calls
    result = result + add(multiply(2, 3), subtract(10, 5));
    
    // Recursive function calls
    result = result + factorial(4);  // 24
    result = result + fibonacci(6);  // 8
    
    // Function with multiple parameters
    result = result + calculate(2, 3, 4);  // 10
    
    // Function with no parameters
    result = result + getConstant();  // 42
    
    // Call a void function
    updateValue(result);
    
    return result; // 130
}