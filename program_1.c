
#include <stdio.h>
#include "set.h"

#define SHARED_VADDR 0x423000


int main(int c, char *argv[]) {

    int id = 1;

    printf("Program %d: Running!\n", id);

    for (int i = 0; i < 5e7; ++i) { if(i % 10000000 == 0) printf("Tick!\n");}
    printf("In program 1 the shared frame store %d\n", *(int*)SHARED_VADDR);

    return 0;
}
