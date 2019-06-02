# Michael Long, Gennadii Sytov -- CS494 -- Server GUI Controller -- May 2019
# Laptop Test

import gui_controller
import server as s

def main():
    
    print('Michael Long, Gennadii Sytov -- CS494: Server')
   
    # Distinguish whether to launch the server locally or online
    print("Server Bootup: Please specify an ip (local: 127.0.0.1, Online: 192.168.0.102)")
    flag = True
    t_host = input()
    if t_host == '127.0.0.1' or t_host == '192.168.0.102':
        flag = False
    while flag:
        print("Server Bootup: Please specify an ip (local: 127.0.0.1, Online: 192.168.0.102)")
        t_host = input()
        if t_host == '127.0.0.1' or t_host == '192.168.0.102':
            flag = False
    
    flag = True
    print("Please specify a port number (local: 1234, Online: 1080)")
    t_port = int(input())
    if t_port == 1234 or t_port == 1080:
        flag = False
    while flag:
        print("Please specify a port number (local: 1234, Online: 1080)")
        t_port = input()
        if t_port == 1234 or t_port == 1080:
            flag = False

    # Launch the server
    server = s.server_handler(host = t_host, port = t_port)
    server.main_loop()

if __name__ == '__main__':
    main()


