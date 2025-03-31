/* Test for recursion */

// Factorial function (recursive)
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Fibonacci function (recursive)
int fibonacci(int n) {
    if (n <= 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// GCD (Greatest Common Divisor) function (recursive)
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

// Sum of digits (recursive)
int sumDigits(int n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) + sumDigits(n / 10);
}

// Main function to test recursion
int main() {
    int result = 0;
    
    // Test factorial
    result = result + factorial(5);  // 5! = 120
    
    // Test fibonacci
    result = result + fibonacci(7);  // fib(7) = 13
    
    // Test GCD
    result = result + gcd(48, 18);  // gcd(48, 18) = 6
    
    // Test sum of digits
    result = result + sumDigits(12345);  // 1+2+3+4+5 = 15
    
    // Test mutual recursion (if supported)
    // result = result + isEven(10);  // Should be 1 (true)
    
    return result;
}

// Mutual recursion example (if supported)
int isEven(int n) {
    if (n == 0) {
        return 1;  // 0 is even
    }
    return isOdd(n - 1);
}

int isOdd(int n) {
    if (n == 0) {
        return 0;  // 0 is not odd
    }
    return isEven(n - 1);
}