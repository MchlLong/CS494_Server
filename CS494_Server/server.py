# Michael Long, Gennadii Sytov -- CS494 -- Server Application -- Server Class

# Imports / Constants
import socket
from _thread import *
import threading
BUFFER = 1024 # Defines the maximum byte size of input from a client

class server_handler():

    def __init__(self, host, port):
        # Basic Socket Variables
        self.host = host
        self.port = port
        self.address = (host, port)
        # Attempt to Bind to Socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        # Data Side
        self.users = {}
        print("Server has initialized (server_handler is ok)")

    def connect(self, connection):
        connection.send(bytes("Hello, please enter a username: ", "utf8"))
        try:
            username = connection.recv(BUFFER).decode("utf8")
            connection.send(bytes("Welcome " + username + " type /? for a list of commands", "utf8"))
            try:
                self.users[connection, username] = connection
                while True:

                    print(username + " is giving data")

                    data = connection.recv(BUFFER)

                    # Check for commands
                    if data == bytes("/?", "utf8"):
                        connection.send(bytes('Commands:\n/join to join a chat room\n/leave to leave a chat room\n/quit to exit',"utf8"))
                    elif data == bytes("/join", "utf8"):
                        print(username + " is going to join a room")
                        # insert join code here
                    elif data == bytes("/leave", "utf8"):
                        print(username + " is going to leave a room")
                        # insert leave code here
                    elif data == bytes("/quit", "utf8"):
                        break
                    else:
                        # Echo to verify functionality
                        print(data)
                        connection.send(data)



                connection.send(bytes("You have been disconnected from the server.", "utf8"))
                del self.users[connection, username]
                connection.close
            except:
                print(username + " has disconnected")
        except:
            print("A user has disconnected")

    def main_loop(self):
        print("The server is listening for a new connection (main_loop has a listener)")
        self.server.listen(5)
        while True:
            print("A connection has been found (main_loop will create a new thread)")
            connection, address = self.server.accept()
            start_new_thread(self.connect, (connection,))
        self.server.close()