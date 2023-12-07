import socketserver
import threading
from datetime import datetime
import json
import Crypto.Hash  # Used to generate keys and for encryption and decryption
import secrets
import string
import oc_database
import re
from tabulate import tabulate
import time
from icecream import ic  # used for debugging
import logging
import sys
from audio import AudioFile
import ffmpeg
import simpleaudio


class Server:
    def __init__(self):
        self.buffer = []
        self.audiofile = AudioFile()
        self.audio_reader = self.audiofile.get_reader()
        self.stop = 0

    def audioStream(self):
        pass

    def playStream(self):
        chunk_count = 0
        while self.buffer:
            print(f"Chunk Count: {chunk_count}")
            chunk = self.buffer.pop(0)
            self.audio_reader.write(chunk)
            chunk_count += 1


udp_server = Server()


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    # Similar to the TCP handler class, except self.request consists of a pair of data and client socket, 
    # Since there is no connection the client address must be given explicitly when sending data back via sendto(). 
    def handle(self):
        # data = self.request[0].strip()
        data = self.request[0]
        current_thread = threading.current_thread()
        # print(f"Current thread: {current_thread}") 
        socket = self.request[1]
        # udp_server.buffer.append(data)
        socket.sendto((bytes("Recieved", 'utf-8')), self.client_address)        
        # chunk = udp_server.buffer.pop(0)
        socket.sendto(data, self.client_address)
        # print(chunk)
        # time.sleep(15)

        # print(data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    print("Called threadedUDPServer")
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9090
    # a = AudioFile()
    # audio_reader = a.getReader()

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    with server:
        try:
            server_thread.start()
            print(f"Server loop running in thread {server_thread.name}")
            print(f"UDP server running on port {PORT}")
            while True:
                command = input(">>> ")
                if command == "/exit":
                    print(f"Shutdown server")
                    server.close()
                    break
                elif command == "/read":
                    udp_server.playStream()

        except Exception as e:
            print(f"Exception: {e}")
