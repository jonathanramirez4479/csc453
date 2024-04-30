import sys

def main():
    arguments = sys.argv

    job_file = arguments[0]
    algorithm = "RR"  # default round robin
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
        else:
            raise ValueError("Wrong input format")
    except ValueError as e:
        print(e)

    print(f"algorithm: {algorithm}\nquantum: {quantum}")


if __name__ == "__main__":
    main()
