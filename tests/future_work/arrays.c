/* Test for arrays */

int main() {
    // Array declaration and initialization
    int numbers[5];
    int result = 0;
    
    // Array element assignment
    numbers[0] = 5;
    numbers[1] = 10;
    numbers[2] = 15;
    numbers[3] = 20;
    numbers[4] = 25;
    
    // Array element access
    result = result + numbers[2];
    
    // Array iteration
    int i;
    for (i = 0; i < 5; i = i + 1) {
        result = result + numbers[i];
    }
    
    // Using array elements in expressions
    int sum = numbers[0] + numbers[1] + numbers[2];
    result = result + sum;
    
    
    return result;
}