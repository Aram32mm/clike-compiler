/* Test for loops */

int main() {
    int result = 0;
    int i;
    
    // While loop
    i = 0;
    while (i < 5) {
        result = result + i;
        i = i + 1;
    }
    
    // For loop
    for (i = 0; i < 5; i = i + 1) {
        result = result + i * 10;
    }
    
    // Nested loops
    for (i = 0; i < 3; i = i + 1) {
        int j;
        for (j = 0; j < 2; j = j + 1) {
            result = result + i * j;
        }
    }
    
    // Loop with break
    i = 0;
    while (i < 10) {
        if (i == 5) {
            break;
        }
        result = result + 1;
        i = i + 1;
    }
    
    // Loop with continue
    for (i = 0; i < 5; i = i + 1) {
        if (i == 2) {
            continue;
        }
        result = result + 100;
    }
    
    return result;  // If all loops work correctly
}