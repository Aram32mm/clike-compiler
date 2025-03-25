// Example demonstrating nested code blocks and scoping
int main() {
    int a = 10;
    
    {
        int b = 20;
        a = a + b;
        
        {
            int c = 30;
            a = a + c;
        }
    }
    
    return a;
}