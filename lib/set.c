int testGlobal = 1009838;
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

int getLocal() {
    return testLocal;
}

void setLocalTo10() {
    doSet(&testLocal, 10);
}

void setLocalTo100() {
    doSet(&testLocal, 100);
}


#define RUBBISH_SIZE 1500000
__attribute__((used)) static char rubbish[RUBBISH_SIZE] = {'a'};
