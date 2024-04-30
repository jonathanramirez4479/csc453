#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"

#define INITIALSTACK 1024

int test_fun(int x)
{
    x = x + 20;
    printf("pid: %d made it to the function test_fun, result: %d\n", lwp_getpid(), x);

    lwp_yield();

    if(lwp_getpid() == 1001)
    {
        printf("\npid 1 is stopping the lwp system\n\n");
        lwp_stop();
    }   

    printf("pid: %d is leaving test_fun...\n", lwp_getpid()); 
    lwp_exit();
}

int func(int x)
{
    printf("pid: %d made it to func not test_fun with arg %d\n", lwp_getpid(), x);
    lwp_yield();
    printf("pid: %d is leaving func...\n");
    lwp_exit();
}

int main()
{
    void* arg = (void *)5;

    int threads[30];

    int i;
    int threads_size = sizeof(threads) / sizeof(threads[0]);

    for(i = 0; i < threads_size; i++) 
    {
        threads[i] = new_lwp(test_fun, (void*)(i + 24), INITIALSTACK);
    }

    lwp_start();

    printf("returned to main\n");

    printf("let's add a new thread and start the processes again\n");
    new_lwp(func, (void*)54, INITIALSTACK);

    lwp_start();
    
    return 0;
}
