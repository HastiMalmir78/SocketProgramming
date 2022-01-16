# SocketProgramming

simple socket programming:

This article describes a very basic one-way Client and Server setup where a Client connects, sends messages to the server and the server shows them using a socket connection.

#Client-Side Programming
Establish a Socket Connection:
To connect to another machine we need a socket connection. A socket connection means the two machines have information about each other’s network location (IP Address) and TCP port. The java.net.Socket class represents a Socket. To open a socket: 
$Socket socket = new Socket(“127.0.0.1”, 5000)

The first argument – IP address of Server. ( 127.0.0.1  is the IP address of localhost, where code will run on the single stand-alone machine).
The second argument – TCP Port. (Just a number representing which application to run on a server. For example, HTTP runs on port 80.  Port number can be from 0 to 65535)
   
#Closing the connection
The socket connection is closed explicitly once the message to the server is sent.

#Server Programming
Establish a Socket Connection

To write a server application two sockets are needed. 

A ServerSocket which waits for the client requests (when a client makes a new Socket())
A plain old Socket socket to use for communication with the client.

#Communication
getOutputStream() method is used to send the output through the socket.

#Close the Connection 
After finishing,  it is important to close the connection by closing the socket as well as input/output streams.


multi clients request with thread:

Server class : The steps involved on server side are similar to the article Socket Programming in Java with a slight change to create the thread object after obtaining the streams and port number.

Establishing the Connection: Server socket object is initialized and inside a while loop a socket object continuously accepts incoming connection. Obtaining the Streams: The inputstream object and outputstream object is extracted from the current requests’ socket object.
Creating a handler object: After obtaining the streams and port number, a new clientHandler object (the above class) is created with these parameters.   Invoking the start() method : The start() method is invoked on this newly created thread object.
ClientHandler class : As we will be using separate threads for each request, lets understand the working and implementation of the ClientHandler class extending Threads. An object of this class will be instantiated each time a request comes. 
First of all this class extends Thread so that its objects assumes all properties of Threads.

Secondly, the constructor of this class takes three parameters, which can uniquely identify any incoming request, i.e. a Socket, a DataInputStream to read from and a DataOutputStream to write to. Whenever we receive any request of client, the server extracts its port number, the DataInputStream object and DataOutputStream object and creates a new thread object of this class and invokes start() method on it.
       
Inside the run() method of this class, it performs three operations: request the user to specify whether time or date needed, read the answer from input stream object and accordingly write the output on the output stream object.

Client Side Programming: Client side programming is similar as in general socket programming program with the following steps-

Establish a Socket Connection
Communication
