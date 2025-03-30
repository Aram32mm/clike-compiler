/* Comprehensive test with all language features */

// Global variables
int global_var = 100;
int global_array[5] = {10, 20, 30, 40, 50};

// Function declarations
int add(int a, int b) {
    return a + b;
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int fib(int n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

// Function that modifies a parameter via pointer
void increment(int *value) {
    *value = *value + 1;
}

// Function that uses global variables
int useGlobal() {
    return global_var + global_array[2];
}

// Main function with all features
int main() {
    // Variable declarations with different types
    int a = 5;
    int b = 10;
    float f = 2.5;
    char c = 'A';
    int result = 0;
    
    // Basic arithmetic
    result = a + b * 2 - 3;  // 5 + 20 - 3 = 22
    
    // Function calls
    result = result + add(a, b);  // 22 + 15 = 37
    
    // Pointers
    int *ptr = &a;
    *ptr = 8;  // a is now 8
    result = result + a;  // 37 + 8 = 45
    
    // Arrays
    int numbers[4];
    numbers[0] = 1;
    numbers[1] = 2;
    numbers[2] = 3;
    numbers[3] = 4;
    
    // Array access
    result = result + numbers[2];  // 45 + 3 = 48
    
    // Loops
    int i;
    for (i = 0; i < 4; i = i + 1) {
        result = result + numbers[i];  // 48 + (1+2+3+4) = 58
    }
    
    // While loop
    i = 0;
    while (i < 3) {
        result = result + 5;  // 58 + 15 = 73
        i = i + 1;
    }
    
    // If-else conditions
    if (a > 7) {
        result = result + 10;  // 73 + 10 = 83
    } else {
        result = result + 5;
    }
    
    // Nested if-else
    if (a > 5) {
        if (b > 5) {
            result = result + 20;  // 83 + 20 = 103
        }
    }
    
    // Logical operators
    if (a > 5 && b < 15) {
        result = result + 25;  // 103 + 25 = 128
    }
    
    if (a > 10 || b > 5) {
        result = result + 30;  // 128 + 30 = 158
    }
    
    // Recursion
    result = result + factorial(4);  // 158 + 24 = 182
    result = result + fib(5);  // 182 + 5 = 187
    
    // Nested blocks and shadowing
    {
        int a = 20;  // Shadows outer a
        result = result + a;  // 187 + 20 = 207
        
        {
            int b = 30;  // Shadows outer b
            result = result + a + b;  // 207 + 20 + 30 = 257
        }
    }
    
    // Global variables
    result = result + global_var;  // 257 + 100 = 357
    result = result + global_array[1];  // 357 + 20 = 377
    
    // Function that uses global vars
    result = result + useGlobal();  // 377 + (100 + 30) = 507
    
    // Pointer function
    increment(&result);  // result is now 508
    
    return result;
}