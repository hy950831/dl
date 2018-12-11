

#include <assert.h>
#include <stdio.h>
#include <sel4/sel4.h>
#include <utils/util.h>

#define SHARED_VADDR 0x422000

int main(int c, char *argv[]) {

    int* t = (int *)SHARED_VADDR;
    *t = 10;

    int id = 2;
    printf("Program %d: Running!\n", id);

    for (int i = 0; i < 1000000; ++i) {}

    printf("In program 2 the shared frame store %d\n", *(int*)SHARED_VADDR);

    return 0;
}
