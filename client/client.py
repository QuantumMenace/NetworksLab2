
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
import os.path 

serverName = '127.0.0.1' 
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
while 1:
	message = raw_input('> ')
	if (message[:6] == ("iWant ")):
		clientSocket.sendto(message, (serverName, serverPort))
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		if (not modifiedMessage): 
			print "receiving file"
			location =  raw_input('Input directory or enter>')
			path = "./received/"
			if (location != ""):
				path = location + "/"
			path = path + message[6:] 
			with open(path, "w+") as f:
				modifiedMessage = " "
				while modifiedMessage:
					modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
					f.write(modifiedMessage)
		else: 
			print modifiedMessage

	elif (message[:6] == ("uTake ")):
		path = message[6:]
		if not os.path.isfile(path):
			print "Failure: What you talkin' bout Willis? I ain't seen that file nowhere!"
		else:	
			clientSocket.sendto(message, (serverName, serverPort))
			with open(path, 'rb') as f:
				data = f.read(2048)
				while data:
					clientSocket.sendto(data, (serverName, serverPort))
					data = f.read(2048)
			clientSocket.sendto("", (serverName, serverPort))
	else:
		clientSocket.sendto(message, (serverName, serverPort))

print "Client Closing"
clientSocket.close()
