

#include <assert.h>
#include <stdio.h>
#include <sel4/sel4.h>
#include <utils/util.h>

#define SHARED_VADDR 0x421000

int main(int c, char *argv[]) {

    int id = 1;
    printf("Program %d: Running!\n", id);


    for (int i = 0; i < 1000000; ++i) {}
    printf("In program 1 the shared frame store %d\n", *(int*)SHARED_VADDR);

    return 0;
}
