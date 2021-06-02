import requests
import logging
import time
import sys
import os

host_arg = sys.argv[1]
port_arg = sys.argv[2]

log = logging.getLogger()


def is_prime(n: int) -> bool:
    """https://en.wikipedia.org/wiki/Primality_test#Python_code"""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def count_prime_number(up_to: int) -> int:
    num = 0
    for i in range(up_to+1):
        if is_prime(i):
            num += 1
    return num


def get_task(url: str):
    log.info('Getting task...')
    r = requests.get(f'{url}/request_task/{os.getpid()}')
    if r.status_code == 204:
        log.debug('Getting task...SKIP')
        return None
    if r.status_code == 200:
        task = r.json()
        log.info(f"Getting task..DONE ({task['number']})")
        return (task['id'], task['number'])
    else:
        print(f"Failed: {r}")
        exit(1)


def send_result(url: str, task_id: int, result: int, time: int) -> bool:
    log.info('Sending result...')
    json = {"task_id": task_id, "result": result, "time": time}
    r = requests.post(f'{url}/send_result', json=json)
    return r.status_code == 200


if __name__ == "__main__":
    url = f"{host_arg}:{port_arg}"

    task_info = get_task(url)
    if not task_info:
        exit(0)
    task_id = task_info[0]
    task_num = task_info[1]

    start_time = time.perf_counter()
    result = count_prime_number(task_num)
    total_time = time.perf_counter() - start_time

    if not send_result(url, task_id, result, total_time):
        log.error("Filed to sending result")
        exit(2)
