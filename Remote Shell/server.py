import socket
import sys


def create_socket():
    """ Declares host name and port number,
        and creates a socket server would be using """
    try:
        global host, port, skt
        host = ""
        port = 9999
        skt = socket.socket()
    except socket.error as err:
        print("Socket creation error:", err)

def bind_socket():
    """ Binds created socket to our host and port
        and receives client's attemt to connect """
    try:
        global host, port, skt
        print("Binding socket to port:", port)
        skt.bind((host, port))
        skt.listen(5)
    except socket.error as err:
        print("Socket binding error:", err)

def accept_socket():
    """ Opens connection to the received client
        and executes commands """
    connection, address = skt.accept()
    print("Connection has been established |", "IP", address[0],\
            "|", "Port", address[1])
    send_command(connection)
    connection.close()

def send_command(connection):
    """ Sends and receives desirable commands
        to the client by the command prompt """
    print("Enter the command (`q` to exit):$ ", end='')
    while True:
        cmd = input()
        if cmd == "q":
            connection.send(cmd.encode())
            connection.close()
            print("Connection is closed")
            sys.exit()
        if cmd:
            connection.send(cmd.encode())
            client_response = connection.recv(1024).decode()
            print(client_response, end='')

def main():
    """ Main function for implementing remote shell
        from the server side """
    create_socket()
    bind_socket()
    accept_socket()


main()
