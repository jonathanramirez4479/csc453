#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"

#define SetBP(bp) asm("movl  %0,%%ebp" : : "r"(bp))

int test_fun(int x)
{
    x = x + 5;
    printf("%d", x);
}

int main()
{
    ptr_int_t *sp = (ptr_int_t *)malloc(8192);

    sp += 2048;
    sp--;

    *sp = (ptr_int_t)5; // argument
    sp--;

    *sp = (ptr_int_t)NULL;
    sp--;

    *sp = (ptr_int_t)test_fun;
    sp--;

    *sp = (ptr_int_t)0xFEEDBEEF;

    ptr_int_t *bp = (ptr_int_t)sp;

    sp -= 7;
    *sp = (ptr_int_t)sp;

    SetSP(sp);
    RESTORE_STATE();

    return 0;
}