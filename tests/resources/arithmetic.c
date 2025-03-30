/* Test for arithmetic operations */

int main() {
    // Basic arithmetic
    int a = 5 + 3;        // Addition
    int b = 10 - 4;       // Subtraction
    int c = 3 * 6;        // Multiplication
    int d = 20 / 5;       // Division
    int e = 11 % 3;       // Modulo
    
    // Compound expressions
    int result1 = (a + b) * c / (d + e);
    
    // Order of operations
    int result2 = 5 + 3 * 2;        // Should be 11, not 16
    int result3 = (5 + 3) * 2;      // Should be 16
    
    // Negative numbers
    int f = -10;
    int g = 7 - -3;                 // Should be 10
    
    // Complex expression
    int result4 = a * (b + c) - d * (e + f) + g;
    
    return result4;
}