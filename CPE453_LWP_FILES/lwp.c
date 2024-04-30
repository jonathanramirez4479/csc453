#include "stdio.h"
#include "lwp.h"
#include "stdlib.h"
#include "errno.h"

const unsigned int WORD_SIZE = 4;
lwp_context lwp_ptable[LWP_PROC_LIMIT]; // table of ready threads
int lwp_procs = 0;
schedfun current_scheduler;  // current scheduler function (either specified by user program or defaulted to round robin)
int pid_start = 1000; // starting pid value for the threads
int lwp_running = -1;
void* original_sp = NULL;  // stack pointer of main thread

int new_lwp(lwpfun func, void *arg, size_t stack_size)
{
    /* This function creates a new thread, appends it to the thread pool and returns it's pid */

   // check if maximum threads are being used
   if (lwp_procs == LWP_PROC_LIMIT)
   {
    return -1;
   }
    
    // create a new thread
    lwp_context* new_thread  = &lwp_ptable[lwp_procs];
    new_thread->pid = pid_start; // set thread PID
    new_thread->stacksize = stack_size;  // set stacksize value
    new_thread->stack = (ptr_int_t*)malloc(stack_size * sizeof(ptr_int_t)); // allocate the thread's stack

    pid_start++; // increment the available PID for the following threads

    // populate the thread stack
    ptr_int_t* sp = new_thread->stack;
    sp += stack_size;
    sp--;

    *sp = (ptr_int_t) arg;  // set the thread's argument
    sp--;

    *sp = (ptr_int_t) exit;  // bogus return address
    sp--;

    *sp = (ptr_int_t) func; // thread's function
    sp--;

    *sp = (ptr_int_t) 0xFEEDBEEF;  // bogus base pointer

    ptr_int_t* bp = sp;
    sp -= 7;  // CPU registers

    *sp = (ptr_int_t) bp;  // sp holds base pointer value

    new_thread->sp = sp;

    // increment the number of ready threads in the pool
    lwp_procs++;

    return new_thread->pid;
}

void lwp_yield()
{
    /* This function is called by a thread to yield control of the CPU to the next thread in the pool */

    SAVE_STATE();  // save the current thread's context on its stack
    GetSP(lwp_ptable[lwp_running].sp);  // store the current thread's sp
    
    int next_thread_index = current_scheduler(); // get the next thread index and update lwp_running
    ptr_int_t* next_thread_sp = lwp_ptable[next_thread_index].sp;

    // restore the next thread in the thread pool
    SetSP(next_thread_sp);
    RESTORE_STATE();
    return;
}

int round_robin()
{
    // round robin scheduler for lwp system
    if(lwp_running == (lwp_procs - 1))
        lwp_running = 0;
    else
        lwp_running++;

    return lwp_running;
}

void lwp_set_scheduler(schedfun sched)
{
    // set the scheduler for the lwp system
    if(sched != NULL)
        current_scheduler = sched;
    else
        current_scheduler = round_robin;
}

void lwp_start()
{
    /* Called by the user program. Starts (or resumes) the LWP system. Saves the original context and stack pointer
     (for lwp_stop or lwp_exit to use later), schedules an LWP, and starts it running. Returns immediately if there are no LWPs.
    */
    SAVE_STATE();
    GetSP(original_sp);

    // check if there is a set scheduler, if not set it to round robin
    if(current_scheduler == NULL)
        current_scheduler = round_robin;

    // if there are no processes in the thread pool, return to main thread
    if (lwp_procs == 0)
    {
        RESTORE_STATE();
        return;
    }
    
    lwp_running = current_scheduler();  // get the next thread in the pool to run

    // restore the selected thread
    SetSP(lwp_ptable[lwp_running].sp);
    RESTORE_STATE();
    return;
}

int lwp_getpid()
{
    // return the pid of the current running thread
    return lwp_ptable[lwp_running].pid;
}

void lwp_exit()
{
    /* this function removes a thread from the process table and moves all others up in the table
    if no threads remain, it restores the current stack point and return to that context */

    lwp_context* current_lwp = &lwp_ptable[lwp_running];

    int next_thread_index = lwp_running; // get the next thread available

    if(lwp_running == (lwp_procs - 1))
    {
        // if the current thread is at the end of the table, remove it, don't move up anything
        current_lwp->pid = 0;
        current_lwp->sp = NULL;
        current_lwp->stacksize = 0;
        free(current_lwp->stack);
        current_lwp->stack = NULL;
        next_thread_index = current_scheduler();
    }
    else
    {
        // otherwise remove the current thread and move up the rest
        current_lwp->pid = 0;
        current_lwp->sp = NULL;
        current_lwp->stacksize = 0;
        free(current_lwp->stack);
        current_lwp->stack = NULL;
        int i;

        // move up the threads in the table
        for(i = lwp_running; i < lwp_procs - 1; i++)
        {
            lwp_ptable[i] = lwp_ptable[i + 1]; // shift left
        }

        lwp_ptable[lwp_procs-1].pid = 0;
        lwp_ptable[lwp_procs-1].sp = NULL;
        lwp_ptable[lwp_procs-1].stack = NULL;
        lwp_ptable[lwp_procs-1].stacksize = 0;
    }

    lwp_procs--;  // decrement the thread count

    if(lwp_procs == 0)
    {
        // if there are no more threads, restore the main thread
        lwp_running = -1;
        SetSP(original_sp);
        RESTORE_STATE();
        return;
    }
    else
    {
        // restore the next thread in the pool
        ptr_int_t* next_thread_sp = lwp_ptable[next_thread_index].sp;

        SetSP(next_thread_sp);
        RESTORE_STATE();
        return;
    }
}

void lwp_stop()
{
    // stop the running LWP system and restore the main thread
    SAVE_STATE();
    GetSP(lwp_ptable[lwp_running].sp);
    SetSP(original_sp);
    RESTORE_STATE();
}