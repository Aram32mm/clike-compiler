// Example demonstrating comparison operators
int main() {
    int a = 10;
    int b = 20;
    int result = 0;
    
    // Equal to
    if (a == 10) {
        result = 1;
    }
    
    // Not equal to
    if (a != b) {
        result = 2;
    }
    
    // Greater than
    if (b > a) {
        result = 3;
    }
    
    // Less than
    if (a < b) {
        result = 4;
    }
    
    // Greater than or equal to
    if (a >= 10) {
        result = 5;
    }
    
    // Less than or equal to
    if (b <= 20) {
        result = 6;
    }
    
    return result;
}