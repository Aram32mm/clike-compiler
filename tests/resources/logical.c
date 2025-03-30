/* Test for logical operators */

int main() {
    int a = 1;  // true
    int b = 0;  // false
    int c = 2;  // true
    int result = 0;
    
    // Logical AND
    if (a && c) {
        result = result + 1;  // Should execute
    }
    
    if (a && b) {
        result = result + 2;  // Should not execute
    }
    
    // Logical OR
    if (a || b) {
        result = result + 4;  // Should execute
    }
    
    if (b || b) {
        result = result + 8;  // Should not execute
    }
    
    // Logical NOT
    if (!b) {
        result = result + 16;  // Should execute
    }
    
    if (!a) {
        result = result + 32;  // Should not execute
    }
    
    // Complex logical expressions
    if (a && !b && c) {
        result = result + 64;  // Should execute
    }
    
    if ((a || b) && (!a || !b)) {
        result = result + 128;  // Should execute
    }
    
    return result;  // Should return 213 if all conditions work correctly
}