/* Test for data types */

int main() {
    // Integer types
    int a = 42;
    
    // Character type
    char c = 'A';
    
    // Floating-point types
    float f = 3.14;
    double d = 2.71828;
    
    // Variable initialization with other variables
    int x = a;
    float y = f;
    
    // Type-specific operations
    int int_result = a * 2;
    float float_result = f * 2.0;
    
    // Casting behavior (if supported)
    // int to float
    float float_from_int = a;
    
    // float to int (truncation expected)
    int int_from_float = f;
    
    // Character arithmetic
    char next_char = c + 1;  // Should be 'B'
    
    // Accumulate results for testing
    int result = a + int_result + int_from_float + next_char;
    
    return result;
}