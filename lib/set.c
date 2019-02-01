int testGlobal = 1009838;
int testGlobal2 = 1009838;
int testGlobal3 = 1009838;

static int testLocal = 0;

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

void setGlobalTo10() {
    testGlobal = 10;
    testGlobal2 = 10;
    testGlobal3 = 10;
}

void setGlobalTo100() {
    testGlobal = 100;
    testGlobal2 = 100;
    testGlobal3 = 100;
}

int getLocal() {
    return testLocal;
}

void setLocalTo10() {
    doSet(&testLocal, 10);
    /* testLocal = 10; */
}

void setLocalTo100() {
    doSet(&testLocal, 100);
    /* testLocal = 100; */
}

