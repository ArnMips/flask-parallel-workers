import subprocess
import sys
import time
import platform

#python .\runner.py http://127.0.0.1 5000 100

host_arg = sys.argv[1]
port_arg = sys.argv[2]
workers_num_arg = int(sys.argv[3])


def run_workers(host: str, port: str, workers_num: int) -> [subprocess.Popen]:
    workers = []
    for _ in range(workers_num):
        prog = "python" if platform.system() == 'Windows' else "python3"
        worker = subprocess.Popen([prog, "worker.py", host, port])
        workers.append(worker)
    return workers


def print_statisticts(workers: [subprocess.Popen]):
    active_worker_num = 0
    finished_worker_num = 0
    failed_workers = []
    for worker in workers:
        retcode = worker.poll()
        if retcode == None:
            active_worker_num += 1
        elif retcode == 0:
            finished_worker_num += 1
        else:
            failed_workers.append([worker.pid, retcode])
    print("-"*10)
    print("Worker status")
    print(f" - active: {active_worker_num}")
    print(f" - finished: {finished_worker_num}")
    print(f" - failed")
    for worker in failed_workers:
        print(f"    - pid:{worker[0]}, ret:{worker[1]}")
    print("")


if __name__ == "__main__":
    workers = run_workers(host_arg, port_arg, workers_num_arg)
    is_running = True
    while is_running:
        time.sleep(1)
        print_statisticts(workers)
        is_running = any([w.poll() == None for w in workers])

    print("DONE. see status above")
