/* Test for complex expressions */

int main() {
    int a = 5;
    int b = 10;
    int c = 15;
    int d = 20;
    int result = 0;
    
    // Complex arithmetic expressions
    result = a * b + c * d;  // 5*10 + 15*20 = 50 + 300 = 350
    
    // Nested expressions with parentheses
    result = result + (a + b) * (c - d);  // (5+10) * (15-20) = 15 * (-5) = -75
    
    // Mixed arithmetic and comparison
    result = result + (a * b > c ? a * b : c * d);  // 5*10 > 15 ? 5*10 : 15*20 = 50 > 15 ? 50 : 300 = 50
    
    // Expressions with function calls (assuming functions are supported)
    result = result + calculateValue(a, b);
    
    // Expressions with side effects
    int temp = 0;
    result = result + (temp = a * b, temp + c);  // temp = 5*10, temp+15 = 50+15 = 65
    
    // Logical expressions
    result = result + (a < b && c < d);  // 5 < 10 && 15 < 20 = true && true = 1
    
    // Complex boolean logic
    result = result + (a < b && c > d || a > b && c < d);  // (true && false) || (false && true) = false || false = 0
    
    // Bit manipulation (if supported)
    result = result + (a & b);  // 5 & 10 = 0
    result = result + (a | b);  // 5 | 10 = 15
    result = result + (a ^ b);  // 5 ^ 10 = 15
    
    return result;
}

// Helper function
int calculateValue(int x, int y) {
    return x * x + y * y;  // 5*5 + 10*10 = 25 + 100 = 125
}