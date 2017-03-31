
setup server
establish socket connection to client

loop for requests
    iWant filename from client
        check that command is correct format (send error if no)
        check if file exists (send error if no)
        send file
