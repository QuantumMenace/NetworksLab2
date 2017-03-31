
"""setup client
establish socket to server

loop for input on command line
    iWant filename
        send request to server
        look for response of file (or error msg)

    uTake filename
        send request to server
        client checks if file exists
        send file when server is ready"""

from socket import *
serverName = '127.0.0.1' 
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowercase sentence:')
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print modifiedMessage
clientSocket.close()
