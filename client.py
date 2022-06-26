# client.py

from socket import *
import sys
import time
import struct

# Implementing various functional requests
class TftpClient(object):
    def __init__(self, sockfd):
        super().__init__()
        self.sockfd = sockfd
        self.opt = ''

    def panel(self):
        print('+', '*'*30, '+', sep='')
        print('+', 'display'.center(30), '+', sep='')
        print('+', 'download'.center(30), '+', sep='')
        print('+', 'upload'.center(30), '+', sep='')
        print('+', 'quit'.center(30), '+', sep='')
        print('+', '*'*30, '+', sep='')

    def display(self):
        self.sockfd.send(b'display')
        print(self.sockfd.recv(1024).decode())

    def download(self):
        'Client download request'
        # First use display The command requests a list of files from the server to verify the existence of the files the user wants to download.
        filename = input('filename>> ')
        if not filename:
            return
        self.sockfd.send(b'display')
        files = self.sockfd.recv(1024).decode().split('\n')
        if not filename in files:
            print('Cannot locate', filename)
            return
        # File exists, send download request to server and receive return result
        data = 'download ' + filename
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(1024).decode()
        # If the server cannot open the file
        if data == 'Failed to open file':
            print('Failed to open file')
        # You can perform download operations
        else:
            # Call write method
            print(data)
            self.write(filename)
            print('Done!')

    def write(self, filename):
        'Download files from the server'
        # Considering the sticking problem, import struct Module, receiving the size of data to be sent by the server, and then according to this size to receive data, circular execution
        fp = open(filename, 'wb')
        while True:
            # Receive data size, call struct.unpack Method to get data size
            res = self.sockfd.recv(4)
            length = struct.unpack('i', res)[0]
            # If the data size is 0, the transfer ends and the loop exits.
            if length == 0:
                break
            # Receiving data by size
            data = self.sockfd.recv(length)
            fp.write(data)
        fp.close()

    def upload(self):
        # File path
        filepath = input('filepath>> ')
        try:
            fp = open(filepath, 'rb')
        except:
            print('Unable to open', filepath)
            return
        else:
            # File upload to save why name
            # First use display The command requests a list of files from the server to verify that the file name that the user wants to upload exists
            filename = input('filename>> ')
            if not filename:
                return
            self.sockfd.send(b'display')
            files = self.sockfd.recv(1024).decode().split('\n')
            if filename in files:
                print('File already exists!')
                return
            # Can upload
            data = 'upload ' + filename
            self.sockfd.send(data.encode())
            data = self.sockfd.recv(1024).decode()
            if data == 'Unable to open file':
                print('Server Open File Error')
                return
            else:
                self.read(fp)

    def read(self, fp):
        'Read File Upload Server'
        while True:
            data = fp.read(1024)
            if not data:
                res = struct.pack('i', 0)
                self.sockfd.send(res)
                break
            res = struct.pack('i', len(data))
            self.sockfd.send(res)
            self.sockfd.send(data)
        print('Done!')

    def quit(self):
        self.sockfd.send(b'quit')
        self.sockfd.close()
        sys.exit('Client shutdown')

# Create sockets, establish connections
def main():
    argc = len(sys.argv)
    if argc != 3:
        sys.exit('Usage: python client.py host port')
    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        ADDR = HOST, PORT

        sockfd = socket()
        try:
            sockfd.connect(ADDR)
        except ConnectionRefusedError:
            sys.exit('Unable to connect to server')

        tftp = TftpClient(sockfd)

        tftp.panel()
        while True:
            try:
                tftp.opt = input('>> ').lower()
            except KeyboardInterrupt:
                tftp.quit()
            if tftp.opt == 'display':
                tftp.display()
            elif tftp.opt == 'download':
                tftp.download()
            elif tftp.opt == 'upload':
                tftp.upload()
            elif tftp.opt == 'quit':
                tftp.quit()
            else:
                continue


if __name__ == '__main__':
    main()