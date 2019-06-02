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
        self.user_count = 0
        print("Server has initialized (server_handler is ok)")

    def connect(self, connection):

        connected = True

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
            self.rooms['General'].append(username)
            connection.send(bytes("You have joined the room!", "utf8"))
            # Assign User Info
            self.users[username] = connection
            print(self.users[username])

            try:

                while connected:

                    print(username + " is giving data")

                    data = connection.recv(BUFFER)
                    scrub_data = data.decode("utf8")
                    print("Decoded Message")
                    # Check for '/' to parse 
                    if scrub_data[0] == '/':
                    # Check for commands
                        
                        # Translate to determine command
                        text = scrub_data.split()
                        for to_print in text:
                            print(to_print)
                        # List set of commands 
                        if text[0] == "/?":
                            connection.send(bytes('Commands:\n/create to make a chat room\n/join to join a chat room\n/leave to leave a chat room\n/users to print each user',"utf8"))
                            connection.send(bytes('/list to show each room\n/disconnect to exit',"utf8"))

                        # Add a user to a room
                        elif text[0] == "/join" and len(text) > 1:
                            print(username + " is going to join a room")
                            flag = False
                            flag_dup = True
                            attempt_room = text[1] 
                            print('Successfully assigned room')

                            # Verify that the room exists
                            for check in self.rooms.keys():
                                print("Scanning room_list")
                                if check == attempt_room:
                                    flag = True

                            # Verify the user is not in the room in the room
                            if flag == True:
                                for check in self.rooms[text[1]]:
                                    print("Looking for duplicates: " + check)
                                    if check == username:
                                        flag_dup = False

                            # If room exists, add the connection to the room
                            if flag == True and flag_dup == True:
                                print("Successfully added to room")
                                self.rooms[attempt_room].append(username)
                                connection.send(bytes("You have joined the room!", "utf8"))
                            # Room exists, but the user is already in the room
                            elif flag == True and flag_dup == False:
                                connection.send(bytes("Error -- you're already in the room", "utf8"))
                            # Room doesn't exist
                            else: 
                                connection.send(bytes("Error -- room does not exist", "utf8"))
                        
                        # Remove a user from a room
                        elif text[0] == "/leave":
                            print(username + " is going to leave a room")
                            flag = False
                            flag_inroom = False
                            attempt_room = text[1] 
                            # Verify that the room exists
                            for check in self.rooms.keys():
                                print("Scanning room_list")
                                if check == attempt_room:
                                    flag = True

                            # Verify the user is in the room
                            if flag == True:
                                for check in self.rooms[text[1]]:
                                    print("Looking for users in room")
                                    if check == username:
                                        flag_inroom = True

                            # Room exists and the user is in the room, leave the room
                            if flag == True and flag_inroom == True:
                                print("Successfully left room")
                                for check in self.rooms[text[1]]:
                                    print(check)
                                self.rooms[attempt_room].remove(username)
                                connection.send(bytes("You have left the room!", "utf8"))
                            # Room exists, user is not in the room, error
                            elif flag == True and flag_inroom == False:
                                connection.send(bytes("Error -- you can't leave a room you're not in", "utf8"))
                            # Room doesn't exist, error
                            else:
                                connection.send(bytes("Error -- room does not exist", "utf8"))

                        # Create a new room
                        elif text[0] == "/create":
                            print(username + " is going to create a room")
                            flag = False
                            flag_roomexists = False
                            # Verify that the room doesn't exist
                            for check in self.rooms.keys():
                                print("Scanning room_list")
                                if check == text[1]:
                                    flag = True
                            if flag == False:
                                print("Created a new room")
                                self.rooms[text[1]] = []

                        # Send a list of usernames
                        elif text[0] == "/users":
                            for to_print in self.users.keys():
                                connection.send(bytes(to_print, "utf8"))

                        # Send a list of all rooms to the user
                        elif text[0] == "/list":
                            for to_send in self.rooms.keys():
                                connection.send(bytes(to_send, "utf8"))

                        # Disconnect a user from a room
                        elif text[0] == "/disconnect":
                            print(username + " has disconnected")
                            del self.users[username]
                            connected = False
                            connection.send(bytes("You have been disconnected from the server.", "utf8"))   
                            self.user_count += 1
                            connection.close
                            return

                        # No valid command was sent, error
                        else:
                            # Echo to verify functionality
                            print(data)
                            connection.send(bytes("Invalid Command", "utf8"))

                    # Send a normal message
                    else:
                        print("Echoing")
                        connection.send(bytes(scrub_data, "utf8"))
                        
            # Client disconnects with a specified username
            except:
                print(username + " has disconnected")
                del self.users[username]
                self.user_count -= 1
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
            connection, address = self.server.accept()
            start_new_thread(self.connect, (connection,))
            print("A connection has been found (main_loop will create a new thread)")
        self.server.close()