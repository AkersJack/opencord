import socketserver


# Makes use of streams (file-like objects that simplify communication by providing the standard file interface)
class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        """
        self.rfile is a file-like object created by the handler
        we can now use e.g. readline() instead of raw recv() calls
        """
        self.data = self.rfile.readline().rstrip()
        print(f"{self.client_address[0]} wrote: ")
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back to the client
        self.wfile.write(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = 'localhost', 12345
    print(f"Server listening on: {PORT}")
    # create the server, binding localhost on port 9999
    # with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; thi swill keep running until you
    # interrupt the program (Ctrl-C)
    server.serve_forever()
