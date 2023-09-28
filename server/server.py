import socketserver
import threading 
from datetime import datetime
import json 
import Crypto.Hash # Used to generate keys and for encryption and decryption


# Versioning 
# Major.Minor.Revision (bug fixes, small updates).build number


# Encryption: 
"""
    - Client generates an asymmetric keypair. 
    - Client sends public key with initial authentication request to server 
    - Server uses the key to encrypt the response and sends back the response to the client
    - If the client is authenticated the server generates a symmetric key and includes that key in the response to the client.  

    * Both the clients asymmetric key and servers symmetric key are "randomly" generated for each connection. 

    
"""
class Client:
    def __init__(self, client_version, profile_hash): # Profile hash can be anything until I develop a hashing method  
        self.client_version = client_version # The client version 
        self.phash = profile_hash # Just going to be a name or something 
        self.connected = datetime.now()
        self.messages = {}
        self.token = None # Need to implement a token 
        self.client_key = None # Clients public key 
        self.private_key = None # The servers private key (or key for this session)
        self.symmetric_key = None # Once encryption is established the server generates a symmetric key

    
    def readMessage(self, message):
        message = json.loads(message)
        t = message.pop('token')
        n = message.pop('n')
         
        self.messages[n] = message
        client = Client("0.0.0.1", self.data)
        return message['content']
    



    
    
    



class Server:
    def __init__(self):
        self.connections = []
        self.server_version = "0.0.0.1"
        self.server_hash = None # Need to implement unique server hashes (easy way for server identification)
        self.verification_hash = None # Need to implement unique verification hashes for the server 
        self.messages = {} # This will be a database in the full version 
    
    
    # Authorize access to the server 
    def authorize(self, user):
        message = {} # holds the auth message
        message["version"] = self.server_version
        message["token"]  = None # Need to implement a token system or session system 

        return message 

    def saveMessages(self, sent, user):
        if user in self.messages.keys():
            self.messages[user] = {**self.messages[user], **sent}
        
        else: 
            self.messages[user] = sent
    
    def loadMessages(self, user):
        if user not in self.messages.keys():
            return 1

        long_string = ">>>  " # Combine all messages into 1 long string (for now )
        user_messages = self.messages[user]
        for message in user_messages.keys():
            long_string += user_messages[message]['content'] + "\n" + ">>>  "
        
        return long_string
    
    
     
    
                
    
opencord_server = Server()
        

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"Client address: {self.client_address}")
        print(f"Request: {self.request}")
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self.data}")
        self.request.sendall(self.data.upper())
        while True: 
            print(f"Socket: {server.socket._closed}")
            # self.data = self.request.recv(1024).strip()
            self.data = self.request.recv(1024)
            if not self.data:
                print("Client Disconnected")
                break
            # print(f"Stripped data: {self.data.strip()}")
            message = self.data.strip()
            message = message.decode('utf-8')
            new_message = "Server says: " + message.upper() + '\n'
            new_message = bytes(new_message, 'utf-8')
         
            print(f"{self.client_address[0]} wrote: {message}")
            self.request.sendall(new_message)
        

class ThreadedTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        message = self.data.strip()
        message = self.data.decode('utf-8')
        msg_object = json.loads(message)
        print(f"{self.client_address[0]} wrote: {self.data}")
        
        client = Client("0.0.0.1", msg_object['profile'])

        print(f"Client address: {self.client_address}")
        print(f"Request: {self.request}")
        # self.data = self.request.recv(1024).strip()
        cur_thread = threading.current_thread()
        print(f"Thread: {cur_thread}")
        # print(f"{self.client_address[0]} wrote: {self.data}")
        # self.request.sendall(self.data.upper())
        loaded_messages = opencord_server.loadMessages(client.phash)
        if loaded_messages != 1:
            self.request.sendall(bytes(loaded_messages, 'utf-8'))
            
        while True: 
            try:
                # print(f"Socket: {server.socket._closed}")
                # self.data = self.request.recv(1024).strip()
                self.data = self.request.recv(1024)
                if not self.data:
                    print("Client Disconnected")
                    opencord_server.saveMessages(client.messages, client.phash)
                    break
                # print(f"Stripped data: {self.data.strip()}")
                message = self.data.strip()
                message = message.decode('utf-8')

                m = client.readMessage(message)

                new_message = "Server says: " + m.upper() + '\n'
                new_message = bytes(m, 'utf-8')
         
                print(f"{self.client_address[0]}: {message}")

                
                self.request.sendall(new_message)
            except Exception as e:
                print(f"Error: {e}")
                opencord_server.saveMessages(client.messages, client.phash)
                break
                
                
                
                
                


# The class should already be defined but we can override functions inside the class
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    print("Called threadedTCPServer")
    pass


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 9090

    # Non threaded server 
    # with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
    #     print("Server Started")
    #     # print(f"Data: {server.fileno()}")
    #     server.serve_forever()


    # Most of this code is from the docs with edits made to it 
    # https://docs.python.org/3/library/socketserver.html
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
    
    with server:
        ip, port = server.server_address
        
        # Start a thread with the server -- that thread will then start
        # one more thread for each request 
        server_thread = threading.Thread(target=server.serve_forever)  # This is the serving thread
        # Exit the server thread when the main thread terminates 

        # The entire Python program exits when only daemon threads are left.
        # So they are abruptly stopped at shutdown meaning resources may not be released properly. 
        # For threads to stop gracefully, they should be non-daemonic and use a signalling mechanism
        # such as an Event.
        server_thread.daemon = True 
        
        server_thread.start()
        
        
        print(f"Server loop running in thread {server_thread.name}")
        while True: 
            try:
                t = input("\"Exit\" to stop the server: ")
                if t == "Exit":
                    break
        
                print("Shutting Down")
                server.shutdown()
            except Exception as e:
                print(f"Error Here: {e}")
                break
        
        server.shutdown() 
            

    