import sys
import sched_lib as slib

class Job:
    def __init__(self, arrival_time, burst_time, job_number):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.job_number = job_number


def sort_jobs(job):
    return (job.arrival_time, job.job_number)


def update_job_numbers(jobs):
    i = 0
    for job in jobs:
        job.job_number = i
        i += 1



def print_jobs(jobs):
    for job in jobs:
        print(vars(job))


def read_jobs(filename):
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
    


def fifo(jobs):
    jobs.sort(key=lambda job: job.arrival_time)

    for job in jobs:
        print(vars(job))

    return jobs



def calculate_average_wait_time(jobs):
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
def calculate_average_turnaround_time(jobs):
    total_turnaround_time = 0
    for job in jobs:
        total_turnaround_time += job.turnaround_time
    return total_turnaround_time / len(jobs)


def output_resulting_jobs(jobs):

    print("Process\t\tarrival time\twait time\t turnaround time\t"
        + f"burst time\tcompletion time")
    for job in jobs:
        print(f"   P{job.job_number} \t\t {job.arrival_time} \t\t"
            + f"{job.wait_time} \t\t {job.turnaround_time}\t\t"
            + f"\t\t{job.burst_time}\t {job.completion_time}")

    
def print_job_metrics(jobs):
    print("Process\twait\tturn-around")
    for job in jobs:
        print(f"P{job.job_number}\t{job.turnaround_time}\t{job.wait_time}")


def main():
    arguments = sys.argv

    try:
        job_file = arguments[1]
    except IndexError as e:
        print("Error: No file argument passed\n")
        return

    algorithm = "FIFO"  # default FIFO
    quantum = 1  # default quantum = 1

    ### TODO: fix how we  input arguments such that -p and -q are taken in any order

    if len(arguments) == 6:
        # schedSim <job-file.txt> -p <ALGORITHM> -q <QUANTUM>
        # OR
        # schedSim <job-file.txt> -q <QUANTUM> -p <ALGORITHM>
        if arguments[2] == "-p":
            algorithm = arguments[3]
            quantum = int(arguments[5])
        elif arguments[2] == '-q':
            quantum = int(arguments[3])
            algorithm = arguments[5]
        else:
            raise ValueError("Invalid flag\n")
    elif len(arguments) == 4:
        # schedSim <job-file.txt> -p <ALGORITHM>
        # OR
        # schedSim <job-file.txt> -q <QUANTUM>
        if arguments[2] == "-p":
            algorithm = arguments[3]
            quantum = 1  # quantum = 1 default
        elif arguments[2] == '-q':
            quantum = int(arguments[3])
        else:
            raise ValueError("Invalid flag\n")
    elif len(arguments) == 2:
        algorithm = "FIFO"
        quantum = 1
    else:
        raise ValueError("Error: not enough or wrongly formatted arguments to run schedSim\n")

    print(f"algorithm: {algorithm}\nquantum: {quantum}")
    jobs = read_jobs(job_file)

    print("before execution:")
    print_jobs(jobs)    

    jobs_finished = slib.simulate_srtn(jobs=jobs)
    jobs_finished.sort(key=sort_jobs)

    print("\nafter execution:")
    print_jobs(jobs_finished)

if __name__ == "__main__":
    main()
