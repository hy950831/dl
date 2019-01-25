int testGlobal = 1009838;

static void doSet(int* in, int num);

void setTo10(int* in) {
    doSet(in, 10);
}

void setTo1(int* in) {
    doSet(in, 1);
}

void setTo2(int* in) {
    doSet(in, 2);
}

static void doSet(int* in, int num) {
    *in = num;
}
