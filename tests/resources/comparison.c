/* Test for comparison operators */

int main() {
    int a = 5;
    int b = 10;
    int c = 5;
    int result = 0;
    
    // Equal to
    if (a == c) {
        result = result + 1;
    }
    
    // Not equal to
    if (a != b) {
        result = result + 2;
    }
    
    // Greater than
    if (b > a) {
        result = result + 4;
    }
    
    // Less than
    if (a < b) {
        result = result + 8;
    }
    
    // Greater than or equal to
    if (a >= c) {
        result = result + 16;
    }
    
    // Less than or equal to
    if (c <= a) {
        result = result + 32;
    }
    
    // Complex comparisons
    if ((a < b) && (b > c)) {
        result = result + 64;
    }
    
    return result;  // 127
}