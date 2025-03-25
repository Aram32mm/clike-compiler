int main() {
    int a;
    int b;
    int c;
    int d;
    int result;

    a = 15;
    b = 7;
    c = 3;
    d = 2;

    int tmp1 = a * b;
    int tmp2 = c / d;
    int tmp3 = tmp1 - tmp2;
    int tmp4 = tmp3 + a;
    int tmp5 = b * c;
    int tmp6 = tmp4 - tmp5;
    result = tmp6 + d;

    return result;
}
