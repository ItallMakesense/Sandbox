from flask import Flask, jsonify, request, abort
import threading
import subprocess
import datetime


app = Flask(__name__)
address = "http://127.0.0.1:5000"

list_of = {"jobs": {}, "statuses": {}, "results": {}}

### Commands executor
def execute(command, job_id, time):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,\
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    ex_code = proc.poll()
    completion_time = datetime.datetime.now()
    completion_day = datetime.date.today().strftime("%A")
    result_id = str(len(list_of["results"]) + 1)
    list_of["results"].setdefault(result_id, {
        "result id": result_id,
        "duration": str(completion_time - time),
        "completed": str(completion_time).replace(" ", completion_day[0]),
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
        "exit code": str(ex_code)
        }
    )
    list_of["statuses"][job_id]["done"] = True
    list_of["statuses"][job_id].setdefault("result id", result_id)

### Unique thread for each job
def job_thread(job_id, time):
    job_thread = threading.Thread(target=execute,args=(\
                    list_of["jobs"][job_id]["command"], job_id, time))
    job_thread.start()

### Working with jobs
#   Gets list of existing jobs
@app.route('/api/jobs', methods=['GET'])
def get_jobs_list():
    return jsonify({"jobs": list(list_of["jobs"].values())})

#   Creates new job for a command
@app.route('/api/jobs', methods=['POST'])
def create_job():
    job_id = str(len(list_of["jobs"]) + 1)
    command = request.json.get("command")
    creation_time = datetime.datetime.now()
    creation_day = datetime.date.today().strftime("%A")
    jobs_start_time.setdefault(job_id, creation_time)
    list_of["jobs"].setdefault(job_id, {
        "job_id": job_id,
        "command": command,
        "created": str(creation_time).replace(" ", creation_day[0])
        }
    )
    list_of["statuses"].setdefault(job_id, {
        "status_id": job_id,
        "done": False
        }
    )
    job_thread(job_id, creation_time)
    return "{} {}\n{}".format(request.environ.get('SERVER_PROTOCOL'),\
            "202 Accepted", job_status_url(job_id))

#   Gets url for checking job status
@app.route('/api/jobs/<job_id>', methods=['GET'])
def job_status_url(job_id):
    if int(job_id) in range(1, len(list_of["statuses"]) + 1):
        return "Location: {}/api/statuses/{}\n".format(address, job_id)
    else:
        return "{} {}".format(request.environ.get('SERVER_PROTOCOL'),\
                "404 Not Found")

#   Removes job from the history
@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def remove_job():
    pass

### Working with jobs statuses
#   Gets execution statuses of jobs
@app.route('/api/statuses', methods=['GET'])
def all_jobs_statuses():
    return jsonify({"statuses": list(list_of["statuses"].values())})

#   Gets execution status of requested job
@app.route('/api/statuses/<job_id>', methods=['GET'])
def job_status(job_id):
    if int(job_id) in range(1, len(list_of["statuses"]) + 1):
        if list_of["statuses"][job_id]["done"]:
            return "{} {}\nLocation: {}\n".format(\
                    request.environ.get('SERVER_PROTOCOL'), "303 See Other",\
                    "{}/api/results/{}".format(address, job_id))
        else:
            return "{} {}\n{}\n".format(request.environ.get('SERVER_PROTOCOL'),\
                    "200 Ok", jsonify(list_of["statuses"][job_id]).data.decode())
    else:
        return "{} {}".format(request.environ.get('SERVER_PROTOCOL'),\
                "404 Not found")

### Working with jobs results
#   Gets list of completed job results
@app.route('/api/results', methods=['GET'])
def all_jobs_results():
    print(list_of["results"])
    return jsonify({"results": list(list_of["results"].values())})

#   Gets job result provided after completion of a job
@app.route('/api/results/<result_id>', methods=['GET'])
def job_result(result_id):
    if int(result_id) in range(1, len(list_of["results"]) + 1):
        print(list_of["results"][result_id])
        return "{} {}\n{}".format(request.environ.get('SERVER_PROTOCOL'),\
                "200 Ok", list_of["results"][result_id])

#   Removes result from the history
@app.route('/api/results/<job_id>', methods=['DELETE'])
def remove_job_result(job_id):
    pass


if __name__ == '__main__':
    app.run()