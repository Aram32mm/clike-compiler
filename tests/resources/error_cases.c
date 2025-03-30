/* Test cases that should produce errors */
/* Note: This file contains intentional errors for testing the compiler's error handling */

// Missing semicolon
int a = 5

// Undeclared variable
int b = c + 5;

// Type mismatch
int d = "string";

// Redeclaration
int e = 10;
int e = 20;

// Invalid array index
int arr[5];
int f = arr[10];

// Division by zero
int g = 10 / 0;

// Missing return in non-void function
int getVal() {
    int x = 10;
    // No return statement
}

// Wrong number of arguments
int add(int x, int y) {
    return x + y;
}

int h = add(1, 2, 3);

// Variable used outside scope
if (a > 0) {
    int scopedVar = 10;
}
int i = scopedVar;

// Invalid type conversion
float pi = 3.14;
char ch = pi;

// Invalid operation
int j = "hello" + "world";

// Break outside of loop
break;

// Continue outside of loop
continue;

// Return outside of function
return 5;

int main() {
    return 0;
}