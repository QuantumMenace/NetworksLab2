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
		request.headers["Connection"] = "close"
		host, port, path = processURL(request.path)

		if request.command == "GET": 
			"Stuff"
			serverRequest = buildRequest(request, host, port, path)
			print serverRequest
			serverSocket = socket(AF_INET, SOCK_DGRAM)
			serverSocket.sendto(serverRequest, (host, int(port)))
			data = serverSocket.recv(1000000)
			print data
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
	if len(parts) >1: 
		host = parts[0]
		port, path = parts[1].split("/", 1)
	else: 
		host, path = parts[0].split("/", 1)
		port = "80"
	path = "/"+path

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


