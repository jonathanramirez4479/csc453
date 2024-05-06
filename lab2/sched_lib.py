"""
schedlib Library

A scheduler library used for simulating jobs
"""

class Job:
    """
    This class represents a job for a scheduler.

    Attributes:
        arrival_time: the time a job arrived 
        burst_time: the number of cycles (processing times) it will need to 
        execute
        wait_time: the time a job spends not executing
        turnaround_time: the time between job arrival and job completion
        job_number: the process id according to when the job arrived
    """
    def __init__(self, arrival_time, burst_time, job_number):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.job_number = job_number


def get_shortest_time_remaining(job):
    """ Returns a job's remaining burst time, used to for SRTN scheduling """
    return job.burst_time


def sort_jobs(job):
    """ key function for Python's bult-in sorting function, used to sort jobs
    from text file depending on arrival time and job number """
    return (job.arrival_time, job.job_number)


def update_job_numbers(jobs):
    """ update's the job numbers after first readthrough of text file 
    (used for consistency in job arrival)"""
    i = 0
    for job in jobs:
        job.job_number = i
        i += 1


def print_jobs(jobs):
    """ prints the member variable values for each Job instance in the list 
    'jobs' """
    for job in jobs:
        print(vars(job))


def read_jobs(filename):
    """ reads in tuples of arrival times and burst times to create a list of 
    jobs and returns that list"""
    jobs = []
    job_index = 0
    with open(filename, 'r') as file:
        for line in file:
            arrival_time, run_time = map(int, line.strip().split())
            jobs.append(Job(arrival_time, run_time, job_index))
            job_index += 1

    jobs.sort(key=sort_jobs)  # sort by arrival && location in file 
    update_job_numbers(jobs)  # update with new job numbers

    return jobs


def update_wait_times(jobs, curr_job_num, curr_burst, curr_cyle):
    """ Goes through each job in a list and updates their wait times, 
    used for SRTN and RR scheduling"""
    for job in jobs:
        if job.job_number != curr_job_num:
            if (curr_cyle - curr_burst) <= job.arrival_time < curr_cyle:  
                # arrived during job execution
                job.wait_time = curr_cyle - job.arrival_time
            elif job.arrival_time < (curr_cyle - curr_burst):  
                # arrived before job execution
                job.wait_time += (curr_burst)


def output_resulting_jobs(jobs):
    """ A function to output the member values for each job in a list of jobs
    (Mostly used for debugging purposes)"""

    print("Process\t\tarrival time\twait time\t turnaround time\t"
        + f"burst time\tcompletion time")
    for job in jobs:
        print(f"   P{job.job_number} \t\t {job.arrival_time} \t\t"
            + f"{job.wait_time} \t\t {job.turnaround_time}\t\t"
            + f"\t\t{job.burst_time}\t {job.completion_time}")

    
def print_job_metrics(jobs):
    """ A function to print out the job number, turnaround time, and wait time
    for each job in a list of jobs"""

    for job in jobs:
        print(f"Job {job.job_number} -- {job.turnaround_time}" + 
              f"  {job.wait_time}")

    print(f"Average -- {sum(job.wait_time for job in jobs) / len(jobs)}"
          + f"  {sum(job.turnaround_time for job in jobs) / len(jobs)}")


def simulate_round_robin(jobs, quantum):
    """ Simulates a list of jobs according to round robin scheduling using 
    a quantum value """

    if len(jobs) == 0:
        print("No jobs to schedule\n")
        exit

    num_jobs = len(jobs)
    jobs_finished = []
    
    cycle = 0
    i = 0
    while len(jobs_finished) < num_jobs:
        job = jobs[i]
        
        burst_remaining = job.burst_time - quantum
        if burst_remaining <= 0:
            cycle += job.burst_time
            job.completion_time = cycle
            update_wait_times(jobs=jobs, curr_job_num=job.job_number, 
                              curr_burst=job.burst_time, curr_cyle=cycle)
            job.burst_time = 0
            job.turnaround_time = job.completion_time - job.arrival_time
            jobs_finished.append(job)
            jobs.remove(job)
            i -= 1
            
        else:
            cycle += quantum
            update_wait_times(jobs=jobs, curr_job_num=job.job_number, 
                              curr_burst=quantum, curr_cyle=cycle)
            job.burst_time = burst_remaining
            

        if len(jobs_finished) < num_jobs and i == len(jobs) - 1:
            i = 0
        else:
            i += 1

    return jobs_finished


def simulate_srtn(jobs):
    """ Simulates a list of jobs according to the Shortest Remaining 
    Time Next algorithm and """

    if len(jobs) == 0:
        print("No jobs to schedule\n")
        exit

    num_jobs = len(jobs)
    jobs_finished = []
    jobs_started = []
    jobs_to_remove = []
    
    cycle = 0
    i = 0
    while len(jobs_finished) < num_jobs:
        for job in jobs:
            if i == job.arrival_time:
                jobs_started.append(job)
                jobs_to_remove.append(job)

        for job in jobs_to_remove:
            jobs.remove(job)

        jobs_to_remove.clear()
        
        if len(jobs_started) == 0:
            i += 1
            continue
        
        job = min(jobs_started, key=get_shortest_time_remaining)
        job.burst_time -= 1

        if job.burst_time == 0:
            job.completion_time = i + 1
            job.turnaround_time = job.completion_time - job.arrival_time
            jobs_finished.append(job)
            jobs_started.remove(job)
        
    
        i += 1
        update_wait_times(jobs=jobs_started, curr_job_num=job.job_number,
                          curr_burst=1, curr_cyle=i)

    return jobs_finished


def calculate_avg_wait_fifo(jobs):
    """ This function calculates the average wait time from a list of jobs 
    scheduled according to the FIFO algorithm; and updates member variables 
    accordingly """
    total_burst_time = 0
    previous_completion_time = 0
    for index, job in enumerate(jobs):
        job.completion_time = previous_completion_time + job.burst_time
        job.turnaround_time = job.completion_time - job.arrival_time
        job.wait_time = max(0, job.turnaround_time - job.burst_time)
        previous_completion_time = job.completion_time
        total_burst_time += job.wait_time
    average_wait_time = total_burst_time / len(jobs)
    return average_wait_time


# can only use this if wait time has been calculated first
def calculate_avg_turnaround_fifo(jobs):
    """ This function calculates the average turnaround time from a list of 
    jobs scheduled according to the FIFO algorithm """

    total_turnaround_time = 0
    for job in jobs:
        total_turnaround_time += job.turnaround_time
    return total_turnaround_time / len(jobs)


