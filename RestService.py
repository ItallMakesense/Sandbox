# -*- coding: utf-8 -*-

"""
HTTP REST service for performing shell commands on a Linux host.

Features:
- Uses only python standard library
- Returns appropriate HTTP codes for responses
- At the same time can be executed a few commands
- Respects Cyrillic alphabet for requests and responses

Examples:
$: curl -i http://localhost:5000/api/jobs
(Client receives "OK" response and json-formatted all jobs list)

$: curl -i -X POST -H 'Content-Type: application/json'\
   -d '{"command": "echo 42"}' http://localhost:5000/api/jobs
(Client recieves "Accepted" response and job status location in header)

$: curl -i http://localhost:5000/api/jobs/1
(Client recieves "OK" response, job status location in header and
 json-formatted job info)

$: curl -i http://localhost:5000/api/statuses
(Client recieves "OK" response and json-formatted statuses for all jobs)

$: curl -i http://localhost:5000/api/statuses/1
(If job wasn't completed, client recieves "OK" respose and
 json-formatted job status. In other case, client recieves "See Other"
 response and job result loction in header)

$: curl -i http://localhost:5000/api/results
(Client recieves "OK" response and json-formatted results for all jobs)

$: curl -i http://localhost:5000/api/results
(Client recieves "OK" response and json-formatted job result)
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import sys
import re
import json
import cgi
import datetime
import subprocess


# Changing encoding to support
# cyrillic alphabet for requests and responses
reload(sys)
sys.setdefaultencoding('utf-8')


class Service(object):

    ip = "localhost"
    port = 5000
    address = ""

    jobs = {}
    statuses = {}
    results = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def spec_response(self, code):
        if code == 200:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        elif code == 404:
            self.send_response(404, "Not Found: job id don\'t exist")
            self.end_headers()
        elif code == 400:
            self.send_response(400, "Bad Request: enter address properly")
            self.end_headers()

###################### METHOD - GET ######################
    def do_GET(self):
###JOBS### Sending jobs list
        if re.search(r'/api/jobs$', self.path):
            self.spec_response(200)
            self.wfile.write(json.dumps({"jobs": Service.jobs.values()},\
                                        indent=2) + "\n")
###STATUSES### Sending jobs status list
        elif re.search(r'/api/statuses$', self.path):
            self.spec_response(200)
            self.wfile.write(json.dumps({"statuses": Service.statuses.values()},\
                                        indent=2) + "\n")
###RESULTS### Sending jobs result list
        elif re.search(r'/api/results$', self.path):
            self.spec_response(200)
            self.wfile.write(json.dumps({"results": Service.results.values()},\
                                        indent=2) + "\n")
###JOB INFO### Sending information about a job
        elif re.search(r'/api/jobs/[^\D]+', self.path):
            job_id = self.path.split('/')[-1]
            self.send_job_info(job_id)
###STATUS### Sending job execution status
        elif re.search(r'/api/statuses/[^\D]+', self.path):
            job_id = self.path.split('/')[-1]
            self.send_status(job_id)
###RESULT### Sending job execution result
        elif re.search(r'/api/results/[^\D]+', self.path):
            result_id = self.path.split('/')[-1]
            self.send_result(result_id)
        else:
            self.spec_response(400)

    def send_job_info(self, job_id): ### Sends information about a job
        if job_id in Service.statuses.keys():
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Locaion", "{}/api/statuses/{}\n".format(\
                                            Service.address, job_id))
            self.end_headers()
            self.wfile.write(json.dumps(Service.jobs[job_id],\
                                        indent=2) + "\n")
        else:
            self.spec_response(404)

    def send_status(self, job_id): ### Sends job execution status
        if job_id in Service.statuses.keys():
# If job execution has completed,
# sending redirection address in job results
            if Service.statuses[job_id]["done"]:
                result_id = Service.statuses[job_id]["result id"]
                self.send_response(303, "See Other: execution completed")
                self.send_header("Content-Type", "application/json")
                self.send_header("Locaion", "{}/api/results/{}\n".format(\
                                            Service.address, result_id))
                self.end_headers()
# If job is still executing, sending job status
            else:
                self.spec_response(200)
            self.wfile.write(json.dumps(Service.statuses[job_id],\
                                        indent=2) + "\n")
        else:
            self.spec_response(404)

    def send_result(self, result_id): ### Sends job execution result
        if result_id in Service.results.keys():
            self.spec_response(200)
            self.wfile.write(json.dumps(Service.results[result_id],\
                                indent=2) + "\n")
        else:
            self.spec_response(404)

###################### METHOD - POST ######################
    def do_POST(self):
###CREATE### Retrieving information about a new job, and creating it
        if re.search(r'/api/jobs$', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
            if ctype == "application/json":
# Getting job content
                length = int(self.headers.getheader("content-length"))
                content = json.loads(self.rfile.read(length))
# Creating job
                self.create_job(content)
            else:
                self.send_response(415)
                self.end_headers()
        else:
            self.spec_response(400)

    def create_job(self, content): ### Creates a new job and executes it in separate thread
        creation_time = datetime.datetime.now()
        creation_day = datetime.date.today().strftime("%A")
        job_id = str(len(Service.jobs) + 1)
# Adding to the jobs list
        Service.jobs.setdefault(job_id, {
            "job_id": job_id,
            "command": content["command"],
            "created": str(creation_time).replace(" ", creation_day[0])})
# Adding to the jobs status list
        self.add_status(job_id)
# Executing new job
        self.execute_in_thread(job_id, creation_time)

    def add_status(self, job_id): ### Adds the job to the status list
        Service.statuses.setdefault(job_id, {
            "status_id": job_id,
            "done": False})
        self.send_response(202)
        self.send_header("Locaion", "{}/api/statuses/{}\n".format(\
                            Service.address, job_id))
        self.end_headers()

    def execute_in_thread(self, job_id, time): ### Executes the job in a new thread
        job_thread = Thread(target=self.execute, args=(\
                            Service.jobs[job_id]["command"], job_id, time))
        job_thread.start()

    def execute(self, command, job_id, time): ### Executes the job and writes it's result
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,\
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ex_code = proc.poll()
# Writing a result of job execution
        result_id = self.add_result(stdout, stderr, ex_code, time)
# Updating jobs status list
        Service.statuses[job_id]["done"] = True
        Service.statuses[job_id].setdefault("result id", result_id)

    def add_result(self, out, err, code, time): ### Writes a result of a job execution
        completion_time = datetime.datetime.now()
        completion_day = datetime.date.today().strftime("%A")
        result_id = str(len(Service.results) + 1)
# Adding result to the jobs result list
        Service.results.setdefault(result_id, {
            "result id": result_id,
            "duration": str(completion_time - time),
            "completed": str(completion_time).replace(" ", completion_day[0]),
            "stdout": out.decode(),
            "stderr": err.decode(),
            "exit code": code })
        return result_id

class Server(object):

    def __init__(self, ip, port):
        self.server = HTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        Service.address = "http://{}".format(":".join(map(str,\
                            self.server.server_address)))
        print "Starting HTTP server at {} (Press CTRL+C to quit)".format(\
                Service.address)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print "\nStopping HTTP server at {}".format(Service.address)
        finally:
            self.server.server_close()
 
if __name__=="__main__":
    server = Server(Service.ip, Service.port)
    server.start()