
"""setup server
establish socket connection to client

loop for requests
    iWant filename from client
        check that command is correct format (send error if no)
        check if file exists (send error if no)
        send file"""

from socket import *
import os.path


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "The server is ready to receive"

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    if (message[:6] == ("iWant ")):
        filename = message[6:]
        path = "./store/"+filename
        if (len(filename.split(" ")) != 1 or not filename): 
        	serverSocket.sendto("That just ain't right!", clientAddress)
        elif not os.path.isfile(path):
        	serverSocket.sendto("Failure: What you talkin' bout Willis? I ain't seen that file nowhere!", clientAddress)
        else: 
        	f = open(path, 'rb')
        	data= f.read()
        	f.close()
        	serverSocket.sendto(data, clientAddress)
    else: 
    	serverSocket.sendto("That just ain't right!", clientAddress)


