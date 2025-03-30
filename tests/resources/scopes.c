/* Test for variable scoping */

int globalVar = 100;

void updateGlobal() {
    globalVar = globalVar + 50;
}

int getGlobal() {
    return globalVar;
}

int main() {
    int result = 0;
    int localVar = 10;
    
    // Access global and local variables
    result = globalVar + localVar;
    
    // Update global variable
    updateGlobal();
    result = result + getGlobal();
    
    // New block scope
    {
        int localVar = 20;  // Shadows outer localVar
        result = result + localVar;
        
        int blockVar = 30;
        result = result + blockVar;
    }
    
    // localVar still has original value
    result = result + localVar;
    
    // blockVar not accessible here
    // result = result + blockVar;  // This would cause a compiler error
    
    // Nested scopes in conditional
    if (localVar > 5) {
        int conditionalVar = 40;
        result = result + conditionalVar;
        
        // Can still access outer variables
        result = result + localVar;
    }
    
    // Loop with its own scope
    for (int i = 0; i < 3; i = i + 1) {
        result = result + i;
        
        // Nested block in loop
        {
            int innerVar = 5;
            result = result + innerVar;
        }
    }
    
    return result;
}