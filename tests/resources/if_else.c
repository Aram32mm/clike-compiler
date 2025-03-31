/* Test for if-else control structures */

int main() {
    int x = 10;
    int y = 20;
    int result = 0;
    
    // Simple if
    if (x < y) {
        result = result + 1;
    }
    
    // If-else
    if (x > y) {
        result = result + 2;
    } else {
        result = result + 4;
    }
    
    // Nested if-else
    if (x == 10) {
        if (y == 20) {
            result = result + 8;
        } else {
            result = result + 16;
        }
    } else {
        if (y == 20) {
            result = result + 32;
        } else {
            result = result + 64;
        }
    }
    
    // Multiple conditions
    if (x >= 5 && y <= 25) {
        result = result + 128;
    }
    
    // Chain of if-else-if
    if (x > 20) {
        result = result + 35;
    } else if (x > 15) {
        result = result + 40;
    } else if (x > 5) {
        result = result + 45;
    } else {
        result = result + 50;
    }
    
    return result;  // 1165 if
}