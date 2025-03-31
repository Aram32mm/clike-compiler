/* Test for variable declarations and operations */

int main() {
    // Basic variable declarations
    int a;
    int b = 5;
    int c = 10;
    
    // Variable assignments
    a = 3;
    b = b + 2;
    c = a * b;
    
    // Multiple declarations
    int x, y, z;
    x = 1;
    y = 2;
    z = 3;
    
    // Expressions with variables
    int result = a + b * c / (x + y);
    
    // Update variables
    result = result + 1;
    
    return result; // 53
}