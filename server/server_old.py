import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for the server
    
    It is instantiated once per connection to the server, and must 
    override the handle() method to implement communication to the client.  
    """

    def handle(self):
        # self.request is the TCP socket connected to the client 

        self.data = self.request.recv(2048).strip()
        print("{} wrote: ".format(self.client_address[0]))
        print(self.data)
        # just send back the same data but upper-cased
        self.request.sendall(self.data.upper())

        # return


if __name__ == "__main__":
    HOST, PORT = 'localhost', 12345
    print(f"Server listening on: {PORT}")

    # create the server, binding localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # Activate the server; thi swill keep running until you 
    # interrupt the program (Ctrl-C)
    server.serve_forever()  # calls handle_request() in an infinite loop
