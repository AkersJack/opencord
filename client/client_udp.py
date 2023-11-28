import socket 
import sys
from datetime import datetime 
import json 
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import threading
import time
import os
import re
import pyaudio 
import wave
from audio import AudioFile # custom function 
from multiprocessing import Process, Queue
import ffmpeg


class Client: 
    def __init__(self, sock) -> None:
        self.buffer = []
        self.sock = sock
        self.flag = True

    def playStream(self): 
        chunk_count = 0
        while self.flag:
            print(f"Chunk Count: {chunk_count}")
            chunk = self.buffer.pop(0)
            self.audio_reader.write(chunk)
            chunk_count += 1
















if __name__ == "__main__":
    # print(audio_stream.readframes(1024))

    HOST, PORT = "", 9090
    # data = " ".join(sys.argv[1:])


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = None
    received = None
    i = 0 
    
    client = Client(sock)
    
    packet_object = {
        # "c": False, # Critical data/message
        "n": None, # Packet Number
        "d": None,   # Packet Data      
    }
    
    

    while data != "/exit":
        data = input(">>> ")
        # data = "/audio"

        if data == "/audio":
            q = Queue()

            # Used to play audio 
            # audio_thread = threading.Thread(target=client.playStream())
            # audio_thread.daemon = True
            p = Process(target=client.playStream)
            p.daemon = True

            a = AudioFile("sample.wav")
            p = a.get_object()
            reader = a.get_reader()
            audio_stream = a.get_stream()
            print(f"Format: {p.get_format_from_width(audio_stream.getsampwidth())}")
            print(f"Channel Count: {audio_stream.getnchannels()}")
            print(f"Rate: {audio_stream.getframerate()}")
            audio_data = audio_stream.readframes(1024)
            # a.play()
            # a = AudioFile("sample.wav")
            # audio_stream = a.getStream()
            # audio_data = audio_stream.readframes(1024)
            # time.sleep(3)
            # print(audio_data)

            # audio_data = audio_stream.readframes(1024)
            while audio_data != b'':
                received = None
                counter = 0
                # print(sys.getsizeof(audio_data)) 
                sock.sendto(audio_data, (HOST, PORT))
                data = sock.recv(4129)
                # print(data == audio_data)
                reader.write(data)
                # received = str(sock.recv(1024), "utf-8").strip()
                # while received != "Recieved":
                #     # print(f"Error not received: {received}")
                #     time.sleep(1)
                #     counter += 1
                #     if counter == 5:
                #         sock.sendto(audio_data, (HOST, PORT)) # Resend the data
                #         counter = 0
                # print("Received")
                audio_data = audio_stream.readframes(1024)
                # sock.sendto(bytes("Ready", 'utf-8'), (HOST, PORT)) # Say we're ready for data

                # data = str(sock.recv(4129)).strip()
                # print(f"Done waiting: {data}")
                # if(sent != data):
                #     time.sleep(15)
                # print(sent == data)



            # sock.sendto(buffer, (HOST, PORT)) 
        else:
            # SOCK_DGRAM is the socket type to user for UDP sockets 
    
            # No connec() call; UDP has no connections. 
            # Data is directly sent to the recipient via sendto(). 
            sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
            received = str(sock.recv(1024), "utf-8")

        print(f"Sent: {data}")
        print(f"Received: {received}")