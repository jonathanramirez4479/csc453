#include "stdio.h"
#include "lwp.h"

int main()
{
    ptr_int_t *sp = (ptr_int_t *)malloc(8192);
    sp += 2048;

    printf("hello world\n");
    return 0;
}