// Example demonstrating loop structures
int main() {
    int i;
    int sum = 0;
    
    // For loop
    for (i = 0; i < 10; i = i + 1) {
        sum = sum + i;
    }
    
    // While loop
    i = 0;
    while (i < 5) {
        sum = sum + i;
        i = i + 1;
    }
    
    return sum;
}