int factorial(int n) {
    if (n <= 1) {
        return n;
    }
    
    return n * factorial(n - 1);
}

// Main function
int main() {
    int result;

    result = factorial(3);

    return result;    
}