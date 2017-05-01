"""
Lab 3 Proxy written by Tim Anderson and Dan McGarry
"""

from socket import *
from shutil import copyfile

from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

import os
import sys

def processRequest(message): 
	request = HTTPRequest(message)
	if request.error_code is not None: 
		statusLine = "HTTP/1.0 " + request.error_code + " " + request.error_message
		return statusLine
	else:
		"if connection is in headers, we want it to be close, else we add it"
		request.headers["connection"] = "close"
		host, port, path = processURL(request.path)

		if request.command == "GET": 
			"Stuff"
			serverRequest = buildRequest(request, host, port, path)
			print serverRequest
			serverSocket = socket(AF_INET, SOCK_STREAM)
			serverSocket.settimeout(15.00)
			serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			serverSocket.connect((host, int(port)))
			serverSocket.send(serverRequest)
			"""serverSocket.sendto(serverRequest, (host, int(port)))"""
			print "Waiting to receive data"
			data = [serverSocket.recv(4096)]
			while data[-1]:
				data.append(serverSocket.recv(4096))
			data = ''.join(data)
			print "Received data"
			print data
			serverSocket.shutdown(1)
			serverSocket.close()
			return data
		else: 
			return notImplemented


def buildRequest(request, host, port, path): 
	requestParts = []
	requestParts.append(request.command + " " + path + " HTTP/1.0")
	requestParts.append("Host: " + host + ":" + port)
	for header in request.headers: 
		print header, request.headers[header]
		requestParts.append(header + ": " + request.headers[header])

	requestParts.append("\r\n")
	return "\r\n".join(requestParts)


def processURL(requestPath): 
	if requestPath.lower().startswith("http://"):
		requestPath = requestPath[7:]
	parts = requestPath.split(":")
	if len(parts) > 1: 
		host = parts[0]
		if "/" in parts[1]:
			port, path = parts[1].split("/", 1)
		else:
			port = parts[1]
			path = ""
	else: 
		if "/" in parts[0]:
			host, path = parts[0].split("/", 1)
			port = "80"
		else:
			host = parts[0]
			port = "80"
			path = ""
	path = "/" + path
	return (host, port, path)
	
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = messageext = text


notImplemented = "Not Implemented, (501)"
bad = "Bad Request, (400)"

childBearingLimit = 100

if (len(sys.argv) != 2):
	print "Incorrect number of arguments."
	sys.exit(2)

port = int(sys.argv[1])

proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(('', port))
proxySocket.listen(100)
print "Proxy ready to handle requests on port " + str(port)

while 1: 
	print "waiting for a connection"
	connection, clientAddress = proxySocket.accept()
	message = connection.recv(1000000)
	if(childBearingLimit):
		childBearingLimit = childBearingLimit -1
		parent = os.fork()
		if not parent: 
			"do childish things here"
			data = processRequest(message)
			proxySocket.sendto(data, clientAddress)
			childBearingLimit = childBearingLimit +1
			os._exit(0)

		else: 
			"nothing really, adults don't do anything"


