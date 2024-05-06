import sys
import sched_lib as slib


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
    jobs = slib.read_jobs(job_file)
    jobs_finished = []
    avg_wait = 0
    avg_turnaround = 0

    if algorithm == "RR":
        jobs_finished = slib.simulate_round_robin(jobs=jobs, quantum=quantum)
    elif algorithm == "SRTN":
        jobs_finished = slib.simulate_srtn(jobs=jobs)
    elif algorithm == "FIFO":
        slib.calculate_avg_wait_fifo(jobs=jobs)
        slib.calculate_avg_turnaround_fifo(jobs=jobs)


    slib.print_job_metrics(jobs=jobs)

if __name__ == "__main__":
    main()
