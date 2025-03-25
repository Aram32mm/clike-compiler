// Example demonstrating complex expressions with parentheses
int main() {
    int a = 5;
    int b = 10;
    int c = 15;
    int d = 20;
    int result;
    
    // Nested expressions with parentheses
    result = (a + b) * (c - d);
    
    // Mixed operators with precedence
    result = a + b * c / d;
    
    // Grouping with parentheses
    result = a * (b + (c * d));
    
    return result;
}