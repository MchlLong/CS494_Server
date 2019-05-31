# Michael Long, Gennadii Sytov -- CS494 -- Server GUI Controller -- May 2019
# Laptop Test

import gui_controller
import server as s

def main():
    print('Michael Long, Gennadii Sytov -- CS494: Server')
    a = s.server_handler(host = '127.0.0.1', port = 1234)
    a.main_loop()


if __name__ == '__main__':
    main()


