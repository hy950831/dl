
#include <stdio.h>
#include <sel4utils/sel4_zf_logif.h>
#include "set.h"

#define SHARED_VADDR 0x422000

int main(int c, char *argv[]) {
    int* t = (int *)SHARED_VADDR;

    int id = 2;
    printf("Program %d: Running!\n", id);

    *t = 10;
    ZF_LOGD("Here");
    ZF_LOGD("setTo10's Addr is %p", &setTo10);
    setTo10(t);

    printf("In program 2 the shared frame store %d\n", *(int*)SHARED_VADDR);

    return 0;
}
