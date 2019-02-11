
#include <stdio.h>
#include <sel4utils/sel4_zf_logif.h>
#include "set.h"
#include <stdint.h>

#define SHARED_VADDR 0x424000

extern int testGlobal;

int main(int c, char *argv[]) {
    int* t = (int *)SHARED_VADDR;
    int id = 2;
    printf("Program %d: Running!\n", id);

    printf("The global variable is %d\n", testGlobal);

    printf("In program 2 the shared frame store before setTo10 %d\n", *(int*)SHARED_VADDR);
    setTo10(t);
    printf("In program 2 the shared frame store after setTo10 %d\n", *(int*)SHARED_VADDR);
    setTo1(t);
    printf("In program 2 the shared frame store after setTo1 %d\n", *(int*)SHARED_VADDR);
    setTo2(t);
    printf("In program 2 the shared frame store after setTo2 %d\n", *(int*)SHARED_VADDR);

    int local = getLocal();
    printf("In program 2 the local store %d\n", local);
    setLocalTo10();
    local = getLocal();
    printf("In program 2 the local store %d\n", local);
    setLocalTo100();
    local = getLocal();
    printf("In program 2 the local store %d\n", local);

    return 0;
}
