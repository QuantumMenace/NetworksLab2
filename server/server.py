
"""
Lab 2 server file written by Tim Anderson and Daniel McGarry
"""

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
			print message
		elif not os.path.isfile(path):
			serverSocket.sendto("Failure: What you talkin' bout Willis? I ain't seen that file nowhere!", clientAddress)
		else: 
			serverSocket.sendto("", clientAddress)
			with open(path, 'rb') as f:
				data = f.read(2048)
				while data:
					serverSocket.sendto(data, clientAddress)
					data = f.read(2048)
			serverSocket.sendto("", clientAddress)
			print "finished sending data"

	elif (message[:6] == ("uTake ")):
		print "receiving file"
		path = "./store/"
		path = path + message.split("/")[-1] 
		with open(path, "w+") as f:
			modifiedMessage = " "
			while modifiedMessage:
				modifiedMessage, clientAddress = serverSocket.recvfrom(2048)
				f.write(modifiedMessage)
	else:
		serverSocket.sendto("That just ain't right!", clientAddress)
		print message


