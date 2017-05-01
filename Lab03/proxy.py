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
		try:
			request.headers["connection"] = "close"
			host, port, path = processURL(request.path)

			if request.command == "GET" or request.command == "HEAD" or request.command = "POST": 
				"Stuff"
				serverRequest = buildRequest(request, host, port, path)
				serverSocket = socket(AF_INET, SOCK_STREAM)
				serverSocket.settimeout(15.00)
				serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
				serverSocket.connect((host, int(port)))
				serverSocket.send(serverRequest)
				"""serverSocket.sendto(serverRequest, (host, int(port)))"""
				data = [serverSocket.recv(4096)]
				while data[-1]:
					data.append(serverSocket.recv(4096))
				data = ''.join(data)
				serverSocket.shutdown(SHUT_RDWR)
				serverSocket.close()
				return data
			else: 
				return notImplemented
		except: 
			return bad		



def buildRequest(request, host, port, path): 
	requestParts = []
	requestParts.append(request.command + " " + path + " HTTP/1.0")
	requestParts.append("Host: " + host + ":" + port)
	for header in request.headers: 
		requestParts.append(header + ": " + request.headers[header])

	requestParts.append("\r\n")

	body_length = int(request.headers.getheader('content-length', 0))
	requestParts.append(request.rfile.read(body_length))

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

if (len(sys.argv) != 2):
	print "Incorrect number of arguments."
	sys.exit(2)

port = int(sys.argv[1])

proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(('', port))
proxySocket.listen(100)

while 1: 
	connection, clientAddress = proxySocket.accept()
	parent = os.fork()
	if not parent: 
		"do childish things here"
		message = connection.recv(1000000)
		data = processRequest(message)
		connection.sendto(data, clientAddress)
		connection.shutdown(SHUT_RDWR)
		connection.close()
		break
	else: 
		"nothing really, adults don't do anything"


