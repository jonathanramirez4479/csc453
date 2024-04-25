#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"

#define SetBP(bp) asm("movl  %0,%%ebp" : : "r"(bp))

int test_fun(int x)
{
    int y = 20;
    x = x + 20;
    printf("pid: %d, result: %d\n", lwp_getpid(), x);
    printf("y = %d\n", y);

    lwp_yield();

    printf("pid: %d is leaving...\n", lwp_getpid());
    printf("y = %d\n", y);
    
    lwp_exit();
}

int main()
{
    void* arg = (void *)5;

    int threads[5];

    int i;
    int threads_size = sizeof(threads) / sizeof(threads[0]);

    for(i = 0; i < threads_size; i++) 
    {
        threads[i] = new_lwp(test_fun, arg, 2048);
    }

    printf("at the start there are %d processes\n", lwp_procs);

    lwp_set_scheduler(NULL);

    lwp_start();

    printf("returned to main\n");
    
    return 0;
}
