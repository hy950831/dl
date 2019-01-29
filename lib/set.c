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

static void dummy_func_1() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_2() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_3() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_4() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_5() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_6() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}
static void dummy_func_7() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}

static void dummy_func_8() {
    for (int i = 0; i < 10; ++i) {
        testGlobal++;
    }
}

void increase() {
    dummy_func_1();
    dummy_func_2();
    dummy_func_3();
    dummy_func_4();
    dummy_func_5();
    dummy_func_6();
    dummy_func_7();
    dummy_func_8();
}

