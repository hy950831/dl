
#include <stdio.h>
#include <sel4utils/sel4_zf_logif.h>
#include "set.h"
#include <stdint.h>

#define SHARED_VADDR 0x424000

#include <elf/elf.h>

/* extern  Elf64_Addr  _GLOBAL_OFFSET_TABLE_[]; */

extern int testGlobal;




int main(int c, char *argv[]) {
    int* t = (int *)SHARED_VADDR;

    int id = 2;
    printf("Program %d: Running!\n", id);

    ZF_LOGD("setTo10's Addr is %p, %zx", &setTo10, *(uint64_t *)&setTo10);
    ZF_LOGD("The global variable is %d", testGlobal);

    printf("In program 2 the shared frame store before setTo10 %d\n", *(int*)SHARED_VADDR);
    setTo10(t);
    printf("In program 2 the shared frame store after setTo10 %d\n", *(int*)SHARED_VADDR);


    setTo1(t);
    printf("In program 2 the shared frame store after setTo1 %d\n", *(int*)SHARED_VADDR);
    setTo2(t);
    printf("In program 2 the shared frame store after setTo2 %d\n", *(int*)SHARED_VADDR);

    return 0;
}
