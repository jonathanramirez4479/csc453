#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"

#define SetBP(bp) asm("movl  %0,%%ebp" : : "r"(bp))

int test_fun(int x)
{
    x = x + 20;
    printf("what did i get? %d\n", x);
}

int main()
{
    int arg[] = {5};
    // ptr_int_t *sp = (ptr_int_t *)malloc(8192);

    // sp += 2048;
    // sp--;

    // *sp = (ptr_int_t) 100; // argument
    // sp--;

    // *sp = (ptr_int_t) exit;
    // sp--;

    // *sp = (ptr_int_t) test_fun;
    // sp--;

    // *sp = (ptr_int_t) 0xFEEDBEEF;

    // ptr_int_t *bp = (ptr_int_t)sp;

    // sp -= 7;
    // *sp = (ptr_int_t)bp;

    // SetSP(sp);
    // RESTORE_STATE();

    // int res = new_lwp((lwpfun)test_fun, (void*) arg, 2048);

    printf("arg: %d\n", *arg);

    
    // free(sp);

    return 0;
}