def update_wait_times(jobs, curr_job_num, curr_burst, curr_cyle):
    for job in jobs:
        if job.job_number != curr_job_num:
            if (curr_cyle - curr_burst) <= job.arrival_time < curr_cyle:  # arrived during job execution
                job.wait_time = curr_cyle - job.arrival_time
            elif job.arrival_time < (curr_cyle - curr_burst):  # arrived before job execution
                job.wait_time += (curr_burst)





def simulate_round_robin(jobs, quantum):
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

        