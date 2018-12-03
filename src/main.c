#include <stdio.h>
#include <sel4/sel4.h>
#include <sel4platsupport/bootinfo.h>
#include <sel4platsupport/platsupport.h>
#include <utils/util.h>

int main(int argc, char const *argv[])
{
    platsupport_serial_setup_bootinfo_failsafe();
    printf("Here\n");
    return 0;
}