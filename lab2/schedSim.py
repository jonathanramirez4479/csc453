import sys

class Job:
    def __init__(self, arrival_time, burst_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.completion_time = 0


def read_jobs(filename):
    jobs = []
    with open(filename, 'r') as file:
        for line in file:
            arrival_time, run_time = map(int, line.strip().split())
            jobs.append(Job(arrival_time, run_time))
    return jobs


def fifo(jobs):
    jobs.sort(key=lambda job: job.arrival_time)
    return jobs

def calculate_average_wait_time(jobs):
    total_burst_time = 0
    for index, job in enumerate(jobs):
        job.completion_time = total_burst_time + job.burst_time
        job.turnaround_time = (job.completion_time - job.arrival_time)
        job.wait_time = max(0, job.turnaround_time - job.burst_time)
        total_burst_time += job.burst_time
    #print(f'{index}: {total_burst_time}')
    average_wait_time = total_burst_time / len(jobs)
    return average_wait_time



# can only use this if wait time has been calculated first
def calculate_average_turnaround_time(jobs):
    total_turnaround_time = 0
    for job in jobs:
        total_turnaround_time += job.turnaround_time
    return total_turnaround_time / len(jobs)



def main():
    arguments = sys.argv

    job_file = arguments[1]
    algorithm = "FIFO"  # default round robin
    quantum = 1  # default quantum = 1
    try:
        if len(arguments) == 6:
            # schedSim <job-file.txt> -p <ALGORITHM> -q <QUANTUM>
            # OR
            # schedSim <job-file.txt> -q <QUANTUM> -p <ALGORITHM>
            if arguments[2] == "-p":
                algorithm = arguments[3]
                quantum = arguments[5]
            elif arguments[2] == '-q':
                quantum = arguments[3]
                algorithm = arguments[5]
            else:
                raise ValueError("Wrong input format")
        elif len(arguments) == 4:
            # schedSim <job-file.txt> -p <ALGORITHM>
            # OR
            # schedSim <job-file.txt> -q <QUANTUM>
            if arguments[2] == "-p":
                algorithm = arguments[3]
                quantum = 1  # quantum = 1 default
            elif arguments[2] == '-q':
                quantum = arguments[3]
            else:
                raise ValueError("Wrong input format")
    except ValueError as e:
        print(e)

    print(f"algorithm: {algorithm}\nquantum: {quantum}")
    jobs = read_jobs(job_file)
    jobs = fifo(jobs)
    print(f"\nAverage Wait Time: {calculate_average_wait_time(jobs)}")
    for job in jobs:
        print(job.arrival_time, job.burst_time, job.wait_time, job.completion_time, job.turnaround_time)
    print(f"\nAverage Turnaround Time: {calculate_average_turnaround_time(jobs)}")

if __name__ == "__main__":
    main()
