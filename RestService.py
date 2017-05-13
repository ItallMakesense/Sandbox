from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import subprocess
import re
import cgi
import json
import datetime


class Service(object):

    ip = "localhost"
    port = 5000
    address = ""

    jobs = {}
    statuses = {}
    results = {}

    # job_id = 0
    # result_id = 0
    # @classmethod
    # def get_job_id(self):
    #     Service.job_id += 1
    #     return str(Service.job_id)
    # @classmethod
    # def get_result_id(self):
    #     Service.job_id += 1
    #     return str(Service.job_id)

 
class HTTPRequestHandler(BaseHTTPRequestHandler):

    def spec_response(self, code):
        if code == 200:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        elif code == 404:
            self.send_response(404, "Not Found: wrong job id")
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
                                        indent=2))
###STATUSES### Sending jobs status list
        elif re.search(r'/api/statuses$', self.path):
            self.spec_response(200)
            self.wfile.write(json.dumps({"statuses": Service.statuses.values()},\
                                        indent=2))
###RESULTS### Sending jobs result list
        elif re.search(r'/api/results$', self.path):
            self.spec_response(200)
            self.wfile.write(json.dumps({"results": Service.results.values()},\
                                        indent=2))
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

### Sends information about a job
    def send_job_info(self, job_id):
        if job_id in Service.statuses.keys():
            self.send_response(200)
            self.send_header("Locaion", "{}/api/statuses/{}\n".format(\
                                            Service.address, job_id))
            self.end_headers()
            self.wfile.write(json.dumps(Service.jobs[job_id],\
                                    indent=2))
        else:
            self.spec_response(404)

### Sends job execution status
    def send_status(self, job_id):
        if job_id in Service.statuses.keys():
# If job has completed, sending address for checking job results
            if Service.statuses[job_id]["done"]:
                result_id = Service.statuses[job_id]["result id"]
                self.send_response(303, "See Other: execution completed")
                self.send_header("Locaion", "{}/api/results/{}\n".format(\
                                            Service.address, result_id))
                self.end_headers()
# If job is still executing, sending job status
            else:
                self.spec_response(200)
                self.wfile.write(json.dumps(Service.statuses[job_id],\
                                    indent=2))
        else:
            self.spec_response(404)

### Sends job execution result
    def send_result(self, result_id):
        if result_id in Service.results.keys():
            self.spec_response(200)
            self.wfile.write(json.dumps(Service.results[result_id],\
                                indent=2))
        else:
            self.spec_response(404)

###################### METHOD - POST ######################
    def do_POST(self):
###CREATE### Posting information of a new job
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

### Creates a new job and executes it in separate thread
    def create_job(self, content):
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

### Adds the job to the status list
    def add_status(self, job_id):
        Service.statuses.setdefault(job_id, {
            "status_id": job_id,
            "done": False})
        self.send_response(202)
        self.send_header("Locaion", "{}/api/statuses/{}\n".format(\
                            Service.address, job_id))
        self.end_headers()

### Executes the job in a new thread
    def execute_in_thread(self, job_id, time):
        job_thread = threading.Thread(target=self.execute, args=(\
                        Service.jobs[job_id]["command"], job_id, time))
        job_thread.start()

### Executes the job and writes it's result
    def execute(self, command, job_id, time):
# Creating subprocess for a job command and executing it
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,\
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ex_code = proc.poll()
# Writing a result of job execution
        completion_time = datetime.datetime.now()
        completion_day = datetime.date.today().strftime("%A")
        result_id = str(len(Service.results) + 1)
# Adding result to the jobs result list
        Service.results.setdefault(result_id, {
            "result id": result_id,
            "duration": str(completion_time - time),
            "completed": str(completion_time).replace(" ", completion_day[0]),
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit code": str(ex_code)})
# Updating jobs status list
        Service.statuses[job_id]["done"] = True
        Service.statuses[job_id].setdefault("result id", result_id)

    def add_result(self, id):
        pass

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
            pass
        print "\nStopping HTTP server at {}".format(Service.address)
        self.server.server_close()
 
if __name__=="__main__":
    server = Server(Service.ip, Service.port)
    server.start()