/* Test for complex expressions */
int main() {
    int a = 1;
    int b = 2;
    int c = 3;
    int d = 4;
    int result = 0;
    
    // Complex arithmetic expressions
    result = a * b + c * d;  
    
    // Nested expressions with parentheses
    result = result + (a + b) * (c - d);  

    // Logical expressions
    result = result + (a < b && c < d); 
    
    // Complex boolean logic
    result = result + (a < b && c > d || a > b && c < d);  

    return result;
}