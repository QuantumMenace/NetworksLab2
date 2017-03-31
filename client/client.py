
setup client
establish socket to server

loop for input on command line
    iWant filename
        send request to server
        look for response of file (or error msg)

    uTake filename
        send request to server
        client checks if file exists
        send file when server is ready
