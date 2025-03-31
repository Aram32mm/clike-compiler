/* Test for pointers */

int main() {
    int a = 5;
    int b = 10;
    int result = 0;
    
    // Pointer declaration and initialization
    int *ptr_a = &a;
    int *ptr_b = &b;
    
    // Dereferencing pointers
    result = result + *ptr_a;  // Should add 5
    result = result + *ptr_b;  // Should add 10
    
    // Modifying values through pointers
    *ptr_a = 15;
    result = result + a;  // Should add 15 (a has been modified)
    
    // Pointer arithmetic (if supported)
    int numbers[5] = {1, 2, 3, 4, 5};
    int *ptr_numbers = numbers;
    
    result = result + *ptr_numbers;  // Should add 1 (first element)
    
    ptr_numbers = ptr_numbers + 2;
    result = result + *ptr_numbers;  // Should add 3 (third element)
    
    // Pointers to pointers (if supported)
    int **ptr_ptr_a = &ptr_a;
    result = result + **ptr_ptr_a;  // Should add 15 (value of a)
    
    // Function pointers (if supported)
    // int (*func_ptr)(int, int) = &add;
    // result = result + func_ptr(3, 4);  // Should add 7
    
    return result;
}

// Helper function for function pointers
int add(int x, int y) {
    return x + y;
}