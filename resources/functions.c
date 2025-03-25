// Example demonstrating function declarations and calls
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int main() {
    int x = 10;
    int y = 5;
    int result;
    
    result = add(x, y);
    result = subtract(x, y);
    
    return result;
}