# server.py

import struct
from socket import *
import os
import signal
import sys
import time

# File Library
FILE_PATH = '/Users/yousefabdolmaleki/Documents/network/'

# Implementing Function Modules
class TftpServer(object):
    def __init__(self, sockfd, addr):
        super().__init__()
        self.sockfd = sockfd
        self.addr = addr
        self.opt = ''

    def display(self):
        re = ''
        for i in os.listdir(FILE_PATH):
            re += i + '\n'
        self.sockfd.send(re.encode())

    def download(self):
        'Function Implementation of Download Module'
        # Try to open the file
        filename = FILE_PATH + self.opt.split(' ')[1]
        print(filename)
        try:
            fp = open(filename, 'rb')
        except:
            self.sockfd.send(b'Failed to open file')
        else:
            self.sockfd.send(b'Ready to transfer')
            # Cyclic sending of data
            while True:
                data = fp.read(1024)
                if not data:
                    # If the transmission is complete, data For empty, transfer 0, jump out of the loop
                    res = struct.pack('i', 0)
                    self.sockfd.send(res)
                    break
                res = struct.pack('i', len(data))
                self.sockfd.send(res)
                self.sockfd.send(data)
            print('Done!')

    def upload(self):
        filename = FILE_PATH + self.opt.split(' ')[1]
        try:
            fp = open(filename, 'wb')
        except:
            self.sockfd.send('Unable to open file'.encode())
        else:
            self.sockfd.send(b'Ready to upload')
            while True:
                res = self.sockfd.recv(4)
                length = struct.unpack('i', res)[0]
                if length == 0:
                    break
                data = self.sockfd.recv(length)
                fp.write(data)
            fp.close()
            print('Done!')


    def quit(self):
        print(self.addr, 'Disconnect')
        self.sockfd.close()
        sys.exit()

# Main stream
def main():
    HOST = '0.0.0.0'
    PORT = 5558
    ADDR = (HOST, PORT)

    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # Notify the kernel that it is not concerned about the end of the child process,Recovered by the kernel.
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('Server exit')
        except Exception as e:
            print(e)
            continue

        print('Successful connection:', addr)

        # Create subprocesses
        pid = os.fork()

        if pid == 0:
            sockfd.close()
            tftp = TftpServer(connfd, addr)
            while True:
                tftp.opt = connfd.recv(1024).decode()
                if tftp.opt == 'display':
                    tftp.display()
                elif tftp.opt.startswith('download'):
                    tftp.download()
                elif tftp.opt.startswith('upload'):
                    tftp.upload()
                elif tftp.opt == 'quit':
                    tftp.quit()
        else:
            connfd.close()
            continue


if __name__ == '__main__':
    main()