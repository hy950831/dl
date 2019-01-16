
#include <stdio.h>
#include <sel4utils/sel4_zf_logif.h>
#include "set.h"
#include <stdint.h>

#define SHARED_VADDR 0x422000

extern int testGlobal;

int main(int c, char *argv[]) {
    int* t = (int *)SHARED_VADDR;

    int id = 2;
    printf("Program %d: Running!\n", id);

    /* *t = 10; */
    /* ZF_LOGD("testGlobal is %d", testGlobal); */
    ZF_LOGD("Here");
    /* ZF_LOGD("setTo10's Addr is %p, %zx", &setTo10, *(uint64_t *)&setTo10); */

    void (*func)(int);
    func = 0x425000;

    /* int *test = 0; */
    /* test = (void*)0x415ff8; */

    /* ZF_LOGD("setTo10's Addr points to %p, %zx", test, *(uint64_t *)func); */
    /* ZF_LOGD("setTo10's plt entry points to %p, %d", test, *test); */
    func(t);

    printf("In program 2 the shared frame store %d\n", *(int*)SHARED_VADDR);

    return 0;
}
