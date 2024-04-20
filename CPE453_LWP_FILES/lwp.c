#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"

const unsigned int WORD_SIZE = 4;
lwp_context lwp_ptable[LWP_PROC_LIMIT];
int lwp_procs = 0;

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

    lwp_ptable[free_thread_index].pid = free_thread_index + 1;
    lwp_ptable[free_thread_index].stacksize = stack_size;

    lwp_ptable[free_thread_index].stack = (ptr_int_t*)malloc(stack_size * WORD_SIZE);

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

    SetSP(sp);
    RESTORE_STATE();

    return EXIT_SUCCESS;

}