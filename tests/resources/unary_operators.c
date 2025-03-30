/* Test for unary operators */

int main() {
    int a = 5;
    int b = 10;
    int result = 0;
    
    // Unary minus
    int c = -a;
    result = result + c;  // Should add -5
    
    // Unary plus (if supported)
    int d = +b;
    result = result + d;  // Should add 10
    
    // Logical NOT
    int e = 0;
    if (!e) {
        result = result + 100;  // Should execute
    }
    
    if (!(a < b)) {
        result = result + 200;  // Should not execute
    }
    
    // Increment/decrement (if supported)
    a = a + 1;  // Equivalent to a++
    result = result + a;  // Should add 6
    
    b = b - 1;  // Equivalent to b--
    result = result + b;  // Should add 9
    
    // Bitwise NOT (if supported)
    // int f = ~a;
    // result = result + f;
    
    // Address-of and dereference (if pointers are supported)
    // int *ptr = &a;
    // int g = *ptr;
    // result = result + g;
    
    return result;
}