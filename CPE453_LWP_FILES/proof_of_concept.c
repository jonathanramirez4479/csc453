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
    void* arg = (void *)5;
    


    // ptr_int_t *sp = (ptr_int_t *)malloc(8192);

    // sp += 2048;
    // sp--;

    // *sp = (ptr_int_t) arg; // argument
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



    // int* threads[5];

    // int i;
    // int threads_size = sizeof(threads) / sizeof(threads[0]);

    // for(i = 0; i <= threads_size; i++) 
    // {
    //     threads[i] = new_lwp(test_fun, arg, 2048);
    // }



    int pid = new_lwp(test_fun, arg, 2048);

    // lwp_set_scheduler(NULL);

    // lwp_start();

    printf("returned back to main\n");
    
    // free(sp);

    return 0;
}
