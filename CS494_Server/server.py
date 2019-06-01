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
        self.rooms = {} # Usage rooms{Room_Name:user_list}
        self.rooms['General'] = []
        self.room_list = []
        self.room_list.append('General')
        self.user_count = 0
        print("Server has initialized (server_handler is ok)")

    def connect(self, connection):

        connected = True
        # for to_print in self.users.keys():
        #    print(to_print)

        try:
            # Add user, get a username to place into data structure
            connection.send(bytes("Hello, please enter a username: ", "utf8"))
            username = connection.recv(BUFFER).decode("utf8")
            # First user, no possibility of duplicates
            if (self.user_count == 0):
                self.user_count += 1
            else:
                # test for duplicate usernames
                flag_entered = False
                flag_repeat = False
                for check in self.users.keys():
                    if check == username:
                        flag_repeat = True
                if flag_repeat == False:
                    pass
                else:
                    while flag_repeat:
                        connection.send(bytes("Username is taken, please enter a valid username: ", "utf8"))
                        username = connection.recv(BUFFER).decode("utf8")
                        flag_repeat = False
                        for check in self.users.keys():
                            if check == username:
                                flag_repeat = True




            # Once a username has been established, welcome and print a series of commands
            connection.send(bytes("Welcome " + username + " type /? for a list of commands", "utf8"))
            # Assign User Info
            self.users[username] = connection
            print(self.users[username])

            try:

                while connected:

                    print(username + " is giving data")

                    data = connection.recv(BUFFER)

                    # Check for commands

                    # List set of commands 
                    if data == bytes("/?", "utf8"):
                        connection.send(bytes('Commands:\n/create to make a chat room\n/join to join a chat room\n/leave to leave a chat room\n/users to print each user',"utf8"))
                        connection.send(bytes('/list to show each room\n/disconnect to exit',"utf8"))

                    # Add a user to a room
                    elif data == bytes("/join", "utf8"):
                        print(username + " is going to join a room")
                        flag = False
                        room = 'Room_A' #parse text for room_id

                        # Verify that the room exists
                        for check in self.room_list():
                            if check == room:
                                flag = True

                        # If room exists, add the connection to the room
                        if flag == True:
                            self.rooms[room].append(connection)
                            for key, val in self.rooms.items():
                                print(key)
                            
                        
                        

                    # Remove a user from a room
                    elif data == bytes("/leave", "utf8"):
                        print(username + " is going to leave a room")
                        # insert leave code here

                    # Send a list of usernames
                    elif data == bytes("/users", "utf8"):
                        for to_print in self.users.keys():
                            connection.send(bytes(to_print, "utf8"))

                    # Send a list of all rooms to the user
                    elif data == bytes("/list", "utf8"):
                        for to_send in self.room_list:
                            connection.send(bytes(to_send, "utf8"))

                    
                    # Disconnect a user from a room
                    elif data == bytes("/disconnect", "utf8"):
                        print(username + " has disconnected")
                        del self.users[username]
                        connected = False
                        connection.send(bytes("You have been disconnected from the server.", "utf8"))               
                        connection.close
                        return

                    # Send a message to each user sharing a room with user
                    else:
                        # Echo to verify functionality
                        print(data)
                        connection.send(data)

            # Client disconnects with a specified username
            except:
                print(username + " has disconnected")
                del self.users[username]
                connection.close()

        # Client disconnects without specifying a username
        except:
            print("A user has disconnected")

    # Main Loop to maintain a connection between a server and client
    def main_loop(self):
        online = True
        print("The server is listening for a new connection (main_loop has a listener)")
        self.server.listen(5)
        while online:
            print("A connection has been found (main_loop will create a new thread)")
            connection, address = self.server.accept()
            start_new_thread(self.connect, (connection,))
        self.server.close()