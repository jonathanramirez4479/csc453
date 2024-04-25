#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"
#include "errno.h"

const unsigned int WORD_SIZE = 4;
lwp_context lwp_ptable[LWP_PROC_LIMIT]; // table of ready threads
int lwp_procs = 0;
schedfun current_scheduler;  // current scheduler function (either specified by user program or defaulted to round robin)
int pid_start = 0; // starting pid value for the threads
int lwp_running = -1;
lwp_context main_context;
void* og_sp = NULL;

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
    
    lwp_context* new_thread  = &lwp_ptable[lwp_procs];
    new_thread->pid = pid_start;
    new_thread->stacksize = stack_size;
    new_thread->stack = (ptr_int_t*)malloc(stack_size * sizeof(ptr_int_t));

    // check if memory allocation failed
    if(new_thread->stack == NULL)
    {
        fprintf(stderr, "Error: Unable to allocate memory for stack: %s\n", strerror(errno));
        return -1;
    }

    pid_start++;

    // populate the thread stack
    ptr_int_t* sp = new_thread->stack;
    sp += stack_size;
    sp--;

    *sp = (ptr_int_t) arg;
    sp--;

    *sp = (ptr_int_t) exit;
    sp--;

    *sp = (ptr_int_t) func;
    sp--;

    *sp = (ptr_int_t) 0xFEEDBEEF;

    ptr_int_t* bp = (ptr_int_t) sp;
    sp -= 7;

    *sp = (ptr_int_t) bp;

    new_thread->sp = sp;

    // increment the number of ready threads in the pool
    lwp_procs++;

    // Use this to test that a new lwp is created correctly and can run
    // SetSP(lwp_ptable[free_thread_index].sp);
    // RESTORE_STATE();

    return new_thread->pid;
}

void lwp_yield()
{
    SAVE_STATE();  // save the current thread's context on its stack
    GetSP(lwp_ptable[lwp_running].sp);  // store the current thread's sp
    
    int next_thread_index = round_robin(); // get the next thread index and update lwp_running
    ptr_int_t next_thread_sp = lwp_ptable[next_thread_index].sp;

    SetSP(next_thread_sp);
    RESTORE_STATE();
    return;
}

int round_robin()
{
    lwp_running++;

    if(lwp_running == lwp_procs)
        lwp_running = 0;
    

    return lwp_running;
}

void lwp_set_scheduler(schedfun sched)
{
    if(sched != NULL)
        current_scheduler = sched;
    else
        current_scheduler = round_robin;
}

void lwp_start()
{
    /* Called by the user program. Starts (or resumes) the LWP system. Saves the original context and stack pointer
     (for lwp_stop or lwp_exit to use later), schedules an LWP, and starts it running. Returns immediately if there are no LWPs.
    
    Notes:
    - save the main thread as a context (globally) in order to return to main context
    */
    SAVE_STATE();
    GetSP(og_sp);

    if (lwp_procs == 0)
    {
        RESTORE_STATE();
        return;
    }
    
    lwp_running = current_scheduler();

    SetSP(lwp_ptable[lwp_running].sp);
    RESTORE_STATE();
    return;
}

int lwp_getpid()
{
    return lwp_ptable[lwp_running].pid;
}

void lwp_exit()
{
    // remove a thread from the process table and move all other's up in the table
    // if no threads remain, it should restore the current stack point and return to that context

    lwp_context* current_lwp = &lwp_ptable[lwp_running];

    int next_thread_index = lwp_running;

    if(lwp_running == LWP_PROC_LIMIT - 1)
    {
        current_lwp->pid = 0;
        current_lwp->sp = NULL;
        current_lwp->stacksize = 0;
        free(current_lwp->stack);
        current_lwp->stack = NULL;
        
        next_thread_index = round_robin();
    }
    else
    {
        current_lwp->pid = 0;
        current_lwp->sp = NULL;
        current_lwp->stacksize = 0;
        free(current_lwp->stack);
        current_lwp->stack = NULL;
        int i;

        for(i = lwp_running; i < lwp_procs - 1; i++)
        {
            lwp_ptable[i] = lwp_ptable[i + 1];
        }

        lwp_ptable[lwp_procs-1].pid = 0;
        lwp_ptable[lwp_procs-1].sp = NULL;
        lwp_ptable[lwp_procs-1].stack = NULL;
        lwp_ptable[lwp_procs-1].stacksize = 0;
    }

    lwp_procs--;

    if(lwp_procs == 0)
    {
        SetSP(og_sp);
        RESTORE_STATE();
        return;
    }
    else
    {
        ptr_int_t next_thread_sp = lwp_ptable[next_thread_index].sp;

        SetSP(next_thread_sp);
        RESTORE_STATE();
        return;
    }
}

void lwp_stop()
{
    SAVE_STATE();
    SetSP(og_sp);
    RESTORE_STATE();
}