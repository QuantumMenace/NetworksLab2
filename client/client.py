
"""
Lab2 Client file written by Tim Anderson and Dan McGarry
"""

from socket import *
from shutil import copyfile
import os

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
			path = "./received/"
			path = path + message[6:] 
			with open(path, "w+") as f:
				modifiedMessage = " "
				while modifiedMessage:
					modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
					f.write(modifiedMessage)
				print "next"
			location =  raw_input('Input directory or enter>')
			if (location != ""): 
				copyfile(path, location+"/"+message[6:])
				os.remove(path)

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
