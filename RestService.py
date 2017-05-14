# -*- coding: utf-8 -*-

"""
HTTP REST service for performing shell commands on a Linux host.
Written for python v.2 usage.

Features:
- Uses only python standard library
- Supports REST methods: GET, POST, DELETE*
- Returns appropriate HTTP codes for responses
- At the same time can be executed a few commands
- Respects Cyrillic alphabet for requests and responses
- Accepts user specified address
  (use "python RestService.py -h" for instructions)

* - DELETE method works on "jobs" and "results" entries

Examples:
$: curl -i http://localhost:5000/api/jobs
(Client receives "OK" response and json-formatted list of all jobs)

$: curl -i -X POST -H 'Content-Type: application/json'\
   -d '{"command": "echo 42"}' http://localhost:5000/api/jobs
(Client recieves "Accepted" response and job status location in header)

$: curl -i http://localhost:5000/api/jobs/1
(Client recieves "OK" response, job status location in header and
 json-formatted job info)

$: curl -i http://localhost:5000/api/statuses
(Client recieves "OK" response and json-formatted statuses of all jobs)

$: curl -i http://localhost:5000/api/statuses/1
(If job wasn't completed, client recieves "OK" respose and
 json-formatted job status. In other case, client recieves "See Other"
 response and job result location in header)

$: curl -i http://localhost:5000/api/results
(Client recieves "OK" response and json-formatted results of all jobs)

$: curl -i http://localhost:5000/api/results/1
(Client recieves "OK" response and json-formatted job result)

$: curl -i -X DELETE http://localhost:5000/api/results/1
(Client recieves "OK" response after successful deletion of a result from list)

$: curl -i -X DELETE http://localhost:5000/api/jobs/1
(Client recieves "OK" response after successful deletion of a job from list)
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import sys
import re
import json
import datetime
import subprocess
import argparse


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

    job_id = 0
    result_id = 0

    @classmethod
    def get_job_id(self):
        self.job_id += 1
        return str(self.job_id)

    @classmethod
    def get_result_id(self):
        self.result_id += 1
        return str(self.result_id)


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.tree = {
        r'/api/jobs$': ("jobs", Service.jobs.values()),
        r'/api/statuses$': ("statuses", Service.statuses.values()),
        r'/api/results$': ("results", Service.results.values())
        }
        self.branches = {
        r'/api/jobs/[^\D]+': ("status id", Service.jobs, self.send_job_info),
        r'/api/statuses/[^\D]+':("statuses", Service.statuses, self.send_status),
        r'/api/results/[^\D]+': ("result id", Service.results, self.send_result)
        }
        return BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

###################### METHOD - GET ######################
    def do_GET(self):
        send = False
# Searching matches with existing major endpoints
        for rgx, res in self.tree.iteritems():
            if re.search(rgx, self.path):
                content = json.dumps({res[0]: res[1]}, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", len(content))
                self.end_headers()
                self.wfile.write(content)
                send = True
                return
# Searching matches with existing id-specified endpoints
        for rgx, res in self.branches.iteritems():
            if re.search(rgx, self.path):
                branch_id = self.path.split('/')[-1]
                self.branch_response(res, branch_id)
                send = True
                return
# No matces with existing endpoints - bad request
        if not send:
            self.send_response(400, "Bad Request: enter address properly")
            self.end_headers()

    def branch_response(self, branch, branch_id):
        if branch_id in branch[1].iterkeys():
# Sending header of request
            content = json.dumps(branch[1][branch_id], indent=2)
            branch[2](len(content), branch_id)
            self.end_headers()
# Sending json-formatted endpoint data
            self.wfile.write(content)
        else:
            self.send_response(404, "Not Found: job with such id don\'t exist")
            self.end_headers()

    def send_job_info(self, length, job_id): ### Sends job endpoint header
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", length)
            self.send_header("Locaion", "{}/api/statuses/{}".format(\
                                            Service.address, job_id))

    def send_status(self, length, job_id): ### Sends status endpoint header
# If job is done, includes redirection link
        if Service.statuses[job_id]["status"] in ("executing", "deleted"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", length)
        elif Service.statuses[job_id]["status"] == "done":
            result_id = Service.statuses[job_id]["result id"]
            self.send_response(303, "See Other: execution had completed")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", length)
            self.send_header("Locaion", "{}/api/results/{}".format(\
                                        Service.address, result_id))

    def send_result(self, length, result_id): ### Sends result endpoint header
        self.send_response(200)
        self.send_header("Content-Type", "application/json")

###################### METHOD - POST ######################
    def do_POST(self):
        if re.search(r'/api/jobs$', self.path):
            if self.headers.getheader("content-type") == "application/json":
# Getting job content
                length = int(self.headers.getheader("content-length"))
                content = json.loads(self.rfile.read(length))
# Creating job
                try:
                    job_id, time = self.create_job(content)
                except:
                    self.send_response(400, "Bad Request: did you use \"command\" key?")
                    self.end_headers()
                else:
# Adding to the jobs status list
                    self.add_status(job_id)
# Sending resonse header
                    self.send_response(202)
                    self.send_header("Locaion", "{}/api/statuses/{}".format(\
                                        Service.address, job_id))
                    self.end_headers()
# Executing new job
                    self.execute_in_thread(job_id, time)
            else:
                self.send_response(415)
                self.end_headers()
        else:
            self.send_response(400, "Bad Request: enter address properly")
            self.end_headers()

    def create_job(self, content): ### Creates a new job and executes it in separate thread
        creation_time = datetime.datetime.now()
        creation_day = datetime.date.today().strftime("%A")
        job_id = Service.get_job_id()
        Service.jobs.setdefault(job_id, {
            "job id": job_id,
            "command": content["command"],
            "created": str(creation_time).replace(" ", creation_day[0])
            })
        return (job_id, creation_time)

    def add_status(self, job_id): ### Adds the job to the status list
        Service.statuses.setdefault(job_id, {
            "status id": job_id,
            "status": "executing"
            })

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
        Service.statuses[job_id]["status"] = "done"
        Service.statuses[job_id].setdefault("result id", result_id)

    def add_result(self, out, err, code, time): ### Writes a result of the job execution
        completion_time = datetime.datetime.now()
        completion_day = datetime.date.today().strftime("%A")
        result_id = Service.get_result_id()
# Adding result to the jobs result list
        Service.results.setdefault(result_id, {
            "result id": result_id,
            "duration": str(completion_time - time),
            "completed": str(completion_time).replace(" ", completion_day[0]),
            "stdout": out.decode(),
            "stderr": err.decode(),
            "exit code": code })
        return result_id

###################### METHOD - DELETE ######################
    def do_DELETE(self):
        proper = False
        for rgx, res in self.branches.iteritems():
# Secure statuses form deletion
            if re.search(rgx, self.path) and res[0] == "statuses":
                proper = True
                self.send_response(403)
                self.end_headers()
                continue
# Searching for matches with existing id-specified endpoints
            elif re.search(rgx, self.path):
                proper = True
                branch_id = self.path.split('/')[-1]
# Deleting entry
                self.delete_item(res, branch_id)
# Updating status
                self.upd_status(res, branch_id)
        if not proper:
            self.send_response(400, "Bad Request: enter address properly")
            self.end_headers()

    def delete_item(self, branch, branch_id):
        deleted = branch[1].pop(branch_id, None)
        if deleted:
            self.send_response(200, "OK: entry deleted")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        else:
            self.send_response(404, "Not Found: job with such id don\'t exist")
            self.end_headers()

    def upd_status(self, branch, branch_id):
        for job_id, status in Service.statuses.iteritems():
            if status[branch[0]] == branch_id:
                Service.statuses[job_id]["status"] = "deleted"
                return


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
    parser = argparse.ArgumentParser(description='HTTP REST Server')
    parser.add_argument('ip', default=Service.ip, nargs='?',\
                        help='HTTP Server IP (127.0.0.1 by default)')
    parser.add_argument('port',type=int, default=Service.port, nargs='?',\
                        help='Port for HTTP Server (5000 by default)')
    args = parser.parse_args()
    server = Server(args.ip, args.port)
    server.start()
