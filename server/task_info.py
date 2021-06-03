from enum import Enum
import json
import os


class TaskStatus(str, Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class TaskInfos():
    def __init__(self) -> None:
        #     [{'status': TaskStatus.TODO.name, worker_pid
        # 'number': 3, 'prime_count': True, 'time': 123}]
        self._dump_file = 'data/tasks_infos.json'
        self._tasks = []  # type: list[dict]
        if not os.path.exists('data'):
            os.mkdir('data')
        if os.path.exists(self._dump_file):
            with open(self._dump_file, 'r') as f:
                self._tasks = json.load(f)

    def _dump(self):
        with open(self._dump_file, 'w') as f:
            json.dump(self._tasks, f)

    def has_data(self):
        return os.path.exists(self._dump_file)

    def get_task(self, worker_pid):
        for i in range(len(self._tasks)):
            if self._tasks[i]['status'] == TaskStatus.TODO:
                self._tasks[i]['status'] = TaskStatus.IN_PROGRESS
                self._tasks[i]['worker_pid'] = worker_pid
                self._dump()
                return {'id': i, 'number': self._tasks[i]['number']}
        return None

    def clean_data(self):
        self._tasks.clear()

    def reset_in_progress(self):
        for task in self._tasks:
            if task['status'] == TaskStatus.IN_PROGRESS:
                task['status'] = TaskStatus.TODO

    def add_task(self, number: int) -> int:
        self._tasks.append({'status': TaskStatus.TODO,
                            'number': number,
                            'prime_count': None,
                            'time': None})
        self._dump()
        return len(self._tasks) - 1

    def add_solution(self, task_id: int, prime_count: int, time: int):
        if self._tasks[task_id]['status'] != TaskStatus.IN_PROGRESS:
            return False
        self._tasks[task_id]['status'] = TaskStatus.DONE
        self._tasks[task_id]['prime_count'] = prime_count
        self._tasks[task_id]['time'] = time
        self._dump()
        return True

    def serialize(self) -> dict:
        task_infos = []
        for i in range(len(self._tasks)):
            task = self._tasks[i]
            task_infos.append(task.copy())
            task_infos[-1]['id'] = i
        task_infos.sort(key=lambda x: -1 if x['time'] == None else x['time'])
        return task_infos
