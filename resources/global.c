// Comprehensive test of C-like language features
// Tests variables, arithmetic, conditionals, loops, functions, expressions, etc.

// Function to calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Function to check if a number is prime
int isPrime(int num) {
    if (num <= 1) {
        return 0; // Not prime
    }
    
    if (num <= 3) {
        return 1; // Prime
    }
    
    if (num % 2 == 0 || num % 3 == 0) {
        return 0; // Not prime
    }
    
    int i = 5;
    while (i * i <= num) {
        if (num % i == 0 || num % (i + 2) == 0) {
            return 0; // Not prime
        }
        i = i + 6;
    }
    
    return 1; // Prime
}

// Function to compute fibonacci
int fibonacci(int n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    
    int a = 0;
    int b = 1;
    int result = 0;
    int i;
    
    for (i = 2; i <= n; i = i + 1) {
        result = a + b;
        a = b;
        b = result;
    }
    
    return result;
}

// Main function with comprehensive test cases
int main() {
    // Variable declarations and initializations
    int x = 10;
    int y = 5;
    int z = 0;
    int result = 0;
    
    // Arithmetic operations
    result = x + y;  // Addition: 15
    result = x - y;  // Subtraction: 5
    result = x * y;  // Multiplication: 50
    result = x / y;  // Division: 2
    
    // Complex expressions with parentheses
    result = (x + y) * (x - y);  // (15) * (5) = 75
    
    // Unary operations
    result = -x;  // -10
    
    // Logical operations
    int flag = 0;
    if (!flag && x > y) {
        result = 100;
    } else {
        result = 200;
    }
    
    // Conditional execution
    if (x > y) {
        // Nested if-else
        if (x > 15) {
            result = 1;
        } else {
            result = 2;
        }
    } else if (x == y) {
        result = 3;
    } else {
        result = 4;
    }
    
    // For loop
    int sum = 0;
    for (int i = 1; i <= 5; i = i + 1) {
        sum = sum + i;
    }  // sum = 15
    
    // While loop
    int j = 10;
    while (j > 0) {
        sum = sum + j;
        j = j - 2;
    }  // sum += 10+8+6+4+2 = 30, total sum = 45
    
    // Nested loops
    int matrix_sum = 0;
    for (int i = 0; i < 3; i = i + 1) {
        for (int j = 0; j < 3; j = j + 1) {
            matrix_sum = matrix_sum + (i * 3 + j);
        }
    }  // sum of 0 to 8 = 36
    
    // Function calls
    int fact5 = factorial(5);  // 120
    int fib10 = fibonacci(10);  // 55
    
    // Prime number test
    int primeCount = 0;
    for (int i = 2; i <= 20; i = i + 1) {
        if (isPrime(i)) {
            primeCount = primeCount + 1;
        }
    }  // primeCount = 8 (2,3,5,7,11,13,17,19)
    
    // Combining results
    int finalResult = fact5 + fib10 + primeCount + sum + matrix_sum;
    
    return finalResult;  // 120 + 55 + 8 + 45 + 36 = 264
}