// Example demonstrating logical operators
int main() {
    int a = 5;
    int b = 10;
    int result = 0;
    
    // Logical AND
    if (a > 0 && b > 0) {
        result = 1;
    }
    
    // Logical OR
    if (a > 10 || b > 5) {
        result = 2;
    }
    
    return result;
}