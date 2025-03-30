/* Test for nested blocks and scoping */

int main() {
    int a = 10;
    int result = 0;
    
    // Simple block
    {
        int b = 20;
        result = result + a + b;  // 10 + 20 = 30
    }
    
    // Variable shadowing
    {
        int a = 30;  // Shadows outer 'a'
        result = result + a;  // 30
        
        {
            int a = 40;  // Shadows middle 'a'
            result = result + a;  // 40
        }
        
        result = result + a;  // Still 30
    }
    
    // Original 'a' is still accessible
    result = result + a;  // 10
    
    // Blocks in if statements
    if (a > 5) {
        int c = 50;
        result = result + c;  // 50
        
        if (a > 8) {
            int d = 60;
            result = result + c + d;  // 50 + 60 = 110
        }
    }
    
    // Blocks in loops
    int i;
    for (i = 0; i < 3; i = i + 1) {
        int e = 70;
        result = result + e;  // 70 + 70 + 70 = 210
        
        {
            int f = 80;
            result = result + f;  // 80 + 80 + 80 = 240
        }
    }
    
    return result;
}