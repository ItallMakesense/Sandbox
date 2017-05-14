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

$: curl -i http://localhost:5000/api/results/1
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

    def __init__(self, *args, **kwargs):
        self.tree = {
        r'/api/jobs$': ("jobs", Service.jobs.values()),
        r'/api/statuses$': ("statuses", Service.statuses.values()),
        r'/api/results$': ("results", Service.results.values())
        }
        self.branches = {
        r'/api/jobs/[^\D]+': ("job", Service.jobs, self.send_job_info),
        r'/api/statuses/[^\D]+':("status", Service.statuses, self.send_status),
        r'/api/results/[^\D]+': ("result", Service.results, self.send_result)
        }
        return BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    
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
        send = False
        while not send:
# Searching matches with existing major endpoints
            for rgx, res in self.tree.items():
                if re.search(rgx, self.path):
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({res[0]: res[1]},\
                                                indent=2) + "\n")
                    send = True
# Searching matches with existing id-specified endpoints
            for rgx, res in self.branches.items():
                if re.search(rgx, self.path):
                    branch_id = self.path.split('/')[-1]
                    self.branch_response(res, branch_id)
                    send = True
# No matces with existing endpoints - bad request
            if not send:
                self.send_response(400, "Bad Request: enter address properly")
                self.end_headers()
                break

    def branch_response(self, branch, branch_id):
        if branch_id in branch[1].keys():
# Sending header of request
            branch[2](branch_id)
            self.end_headers()
# Sending json-formatted endpoint data
            self.wfile.write(json.dumps(branch[1][branch_id],\
                                        indent=2) + "\n")
        else:
            self.send_response(404, "Not Found: job id don\'t exist")
            self.end_headers()

    def send_job_info(self, job_id): ### Sends job endpoint header
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Locaion", "{}/api/statuses/{}".format(\
                                            Service.address, job_id))

    def send_status(self, job_id): ### Sends status endpoint header
# If job is done, includes redirection link
            if Service.statuses[job_id]["done"]:
                result_id = Service.statuses[job_id]["result id"]
                self.send_response(303, "See Other: execution completed")
                self.send_header("Content-Type", "application/json")
                self.send_header("Locaion", "{}/api/results/{}".format(\
                                            Service.address, result_id))
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")

    def send_result(self, result_id): ### Sends result endpoint header
            self.send_response(200)
            self.send_header("Content-Type", "application/json")

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
                job_id, time = self.create_job(content)
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
        job_id = str(len(Service.jobs) + 1)
        Service.jobs.setdefault(job_id, {
            "job_id": job_id,
            "command": content["command"],
            "created": str(creation_time).replace(" ", creation_day[0])
            })
        return (job_id, creation_time)

    def add_status(self, job_id): ### Adds the job to the status list
        Service.statuses.setdefault(job_id, {
            "status_id": job_id,
            "done": False
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