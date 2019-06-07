# Server Implementation
# Implementation of the server_handler 
# Michael Long, Gennadii Sytov
# CS494 Final Project, June 2019

# Imports / Constants
import socket
import _thread

BUFFER = 1024 # Defines the maximum byte size of input from a client

class server_handler():

    def __init__(self, host, port):
        # Basic socket setup
        self.host = host
        self.port = port
        self.address = (host, port)
        # Attempt to bind to socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        # Data
        self.users = {} # Key is a user name, value is an address
        self.rooms = {} # Key is a room name, value is a list of users in the room
        self.rooms['General'] = []
        self.user_count = 0
        self.commands = ['/create ', '/join ', '/leave ', '/users', '/users ', '/list', '/s room_name ', '/w username ', '/disconnect']
        self.commands_usage = ['room_name', 'room_name', 'room_name', '', 'room_name', '', 'room_name message', 'username message', '']
        self.commands_desc = ['creates a new room', 'joins room_name', 'leaves room_name', 'list all users', 'list all users in room_name', 'list all rooms', 'send a message to all users in room_name', 'send a private message to a user', 'disconnect from the server']
        print("Server has initialized (server_handler is ok)")

    def connect(self, connection):

        connected = True

        try:
            # Add user, get a username to place into data structure
            connection.send(bytes("Successfully connected to the Server", "utf8"))
            connection.send(bytes("Please enter a unique username: ", "utf8"))
            username = connection.recv(BUFFER).decode("utf8")

            # Check for null information sent in the connection buffer
            if username == '':
                print("Detected null user")
                return

            # First user, no possibility of duplicates
            if (self.user_count == 0):
                self.user_count += 1
            else:
                # Test for duplicate usernames
                flag_entered = False
                flag_repeat = False
                for check in self.users.keys():
                    if check == username:
                        flag_repeat = True

                # Duplicate username detected, keep checking until a unique username is given
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
            connection.send(bytes("You have joined the room: General", "utf8"))
            # Assign User Info
            self.users[username] = connection
            print(self.users[username])

            try:

                while connected:

                    print(username + " is giving data")
                    # Receive a message from a user
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
                            for (print_command, print_usage, print_desc) in zip(self.commands, self.commands_usage, self.commands_desc):
                                if print_command == self.commands[0] or print_command == self.commands[len(self.commands)-1]:
                                    connection.send(bytes(print_command + print_usage + " -- " + print_desc, "utf8"))
                                else:
                                    connection.send(bytes(print_command + print_usage + " -- " + print_desc + '\n', "utf8"))

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
                                    connection.send(bytes("Error -- room already exists", "utf8"))
                            if flag == False:
                                print("Created a new room")
                                self.rooms[text[1]] = []
                                connection.send(bytes("You successfully created a new room!", "utf8"))


                        # Send a list of usernames
                        elif text[0] == "/users" and len(text) == 1:
                            for to_print in self.users.keys():
                                connection.send(bytes(to_print, "utf8"))

                        # Send a list of usernames in a room
                        elif text[0] == "/users" and len(text) == 2:
                            for room_name, room_list in self.rooms.items():
                                if room_name == text[1]:
                                    for to_send in room_list:
                                        connection.send(bytes(to_send, "utf8"))

                        # List all rooms
                        elif text[0] == "/list":
                            for to_send in self.rooms.keys():
                                connection.send(bytes(to_send, "utf8"))
                        
                        
                        # Disconnect a user from a room
                        elif text[0] == "/disconnect":
                            print("Command: " + username + " has disconnected")
                            connection.send(bytes("--disconnect--", "utf8"))   
                            self.user_count -= 1
                            # Delete all instances of the user in each room
                            for room_name, room_check in self.rooms.items(): # Check each room for it's userlist
                                for user_check in room_check: # Check each userlist
                                    if user_check == username: # If username is in the list of users
                                        room_check.remove(user_check)
                                        print("Successfully removed user from: " + room_name)
                            # Clean up data
                            del self.users[username]
                            print("Successfully deleted user")
                            connected = False
                            connection.close()
                            print("Successfully closed connection")
                            # Close thread
                            return

                        # Send a message to a room
                        elif text[0] == '/s' and len(text) > 2:
                            print(username + " is messaging a specific room")
                            # Verify the room exists, if the room exists join all non-command text
                            for room_name, room_check in self.rooms.items():
                                if room_name == text[1]:
                                    print(text[2::])
                                    each_message = " "
                                    each_message = each_message.join(text[2::])
                                    # For each user in matching room, send the message
                                    for user_check in room_check:
                                        self.users[user_check].send(bytes("(" + room_name + ") " + username + ": " + each_message, "utf8"))

                        # Send a private message to a user
                        elif text[0] == '/w' and len(text) > 2:
                            print(username + " is messaging a specific user")
                            # Verify user exists, if user have been found join all non-command text and send the message
                            for user_key, user_value in self.users.items():
                                if text[1] == user_key:
                                    each_message = " "
                                    each_message = each_message.join(text[2::])
                                    self.users[user_key].send(bytes("(Private To: " + user_key + ") " + username + ": " + each_message, "utf8"))
                            
                        # No valid command was sent, error
                        else:
                            # Echo to verify functionality
                            print(data)
                            connection.send(bytes("Invalid Command", "utf8"))

                    # Send a normal message
                    else:
                        print("Echoing")
                        # Check each room for it's userlist
                        for room_name, room_check in self.rooms.items(): 
                            # Check each userlist in each room
                            for user_check in room_check: 
                                # Check if username is in the list of users
                                if user_check == username: 
                                    print("User matching: " + user_check)
                                    # Send the message to all users who share a room with the sending user
                                    for shared_users in room_check:
                                        print("Shared Users: " + shared_users)
                                        print(self.users.keys())
                                        print(self.users[shared_users])
                                        self.users[shared_users].send(bytes("(" + room_name + ") " + username + ": " + scrub_data, "utf8"))
                                        
                        
            # Client disconnects with a specified username
            except:
                print(username + " has disconnected")
                # Delete all instances of the user in each room
                for room_name, room_check in self.rooms.items(): # Check each room for it's userlist
                    for user_check in room_check: # Check each userlist
                        if user_check == username: # If username is in the list of users
                            room_check.remove(user_check)
                # Clean up connection
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
            _thread.start_new_thread(self.connect, (connection,))
            print("A connection has been found (main_loop will create a new thread)")
        self.server.close()