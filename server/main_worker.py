from flask import Flask, render_template, make_response, request
from flask.json import jsonify
import random
import logging

from werkzeug.wrappers import response
from task_info import TaskInfos

task_infos = TaskInfos()
log = logging.getLogger()
app = Flask(__name__)


def generate_data():
    # return [random.randint(1000000, 5000000) for _ in range(count)]
    data_num = 20
    data = [random.randint(1000, 2000000) for _ in range(data_num)]
    for d in data:
        task_infos.add_task(d)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/table')
def task_table():
    return render_template('task_table.html', task_infos=task_infos.serialize())


@app.route('/add_task/<int:number>')
def add_task(number):
    task_id = task_infos.add_task(number)
    return make_response({'msg': f"Task #{task_id} was added!"}, 200)


@app.route('/reset_in_progress')
def reset_in_progress():
    task_infos.reset_in_progress()
    return make_response({'msg': "OK"}, 200)


@app.route('/reset_data')
def reset_data():
    task_infos.clean_data()
    generate_data()
    return make_response({'msg': "OK"}, 200)


@app.route('/request_task/<int:worker_pid>')
def request_task(worker_pid):
    task_desc = task_infos.get_task(worker_pid)
    if task_desc:
        r = make_response(jsonify(**task_desc), 200)
    else:
        r = make_response({'msg': 'No content'}, 204)
    return r


@app.route('/send_result', methods=['POST'])
def send_result():
    """ Expected:
        {
            "task_id": 1,  
            "result": 123, <prime number count
            "time": 145, < sec
        }
    """
    data = request.get_json()
    task_id = int(data['task_id'])
    result = int(data['result'])
    time = int(data['time'])
    status = task_infos.add_solution(task_id, result, time)
    return make_response({'msg': status}, 200)


if __name__ == "__main__":
    if task_infos.has_data():
        log.info(f"Loading data...")
    else:
        log.info(f"Generating data samples...")
        generate_data()

    log.info("Running server...")
    # app.run(host='0.0.0.0', port=8000)
    app.run()
