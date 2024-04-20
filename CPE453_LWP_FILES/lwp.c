#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"
#include "errno.h"

const unsigned int WORD_SIZE = 4;
lwp_context lwp_ptable[LWP_PROC_LIMIT];
int lwp_procs = 0;
schedfun current_scheduler;
int lwp_running = 29;

int new_lwp(lwpfun func, void *arg, size_t stack_size)
{
    /*
    Notes:
    - stacksize is the word size
    - create a thread and store the data in the struct
    - return the process id of the newly allocated thread
        or -1 if more than LWP_PROC_LIMIT threads already exist
    */

   // check if maximum threads are being used
   if (lwp_procs == LWP_PROC_LIMIT)
   {
    return -1;
   }

   int free_thread_index;
   int i;
    
    // find an unused thread in the thread pool
    for(i = 0; i <= LWP_PROC_LIMIT; i++)
        if(lwp_ptable[i].stack == NULL)
        {
            free_thread_index = i;
            break;
        }

    // populate lwp struct member variables
    lwp_ptable[free_thread_index].pid = free_thread_index;
    lwp_ptable[free_thread_index].stacksize = stack_size;

    lwp_ptable[free_thread_index].stack = (ptr_int_t*)malloc(stack_size * WORD_SIZE);

    // check if memory allocation failed
    if(lwp_ptable[free_thread_index].stack == NULL)
    {
        fprintf(stderr, "Error: Unable to allocate memory for stack: %s\n", strerror(errno));
        return -1;
    }

    // populate the thread stack
    ptr_int_t* sp = lwp_ptable[free_thread_index].stack;
    lwp_ptable[free_thread_index].sp = sp;
    sp += (stack_size * WORD_SIZE);

    *sp = (ptr_int_t*)(arg);
    sp--;

    *sp = (ptr_int_t) exit;
    sp--;

    *sp = (ptr_int_t) func;
    sp--;

    *sp = (ptr_int_t) 0xFEEDBEEF;

    ptr_int_t* bp = (ptr_int_t) sp;
    sp -= 7;

    *sp = (ptr_int_t) bp;

    // increment the number of ready threads in the pool
    lwp_procs++;

    SAVE_STATE();

    return lwp_ptable[free_thread_index].pid;
}

int round_robin()
{
    if(lwp_running == 29)
        lwp_running = 0;
    else
        lwp_running++;

    return lwp_running
}

void lwp_set_scheduler(schedfun sched)
{
    if(sched)
        current_scheduler = sched;
    else
        current_scheduler = round_robin;
}

void lwp_start()
{
    // start the schedular
    lwp_running = current_scheduler();

    // run until no more threads

}