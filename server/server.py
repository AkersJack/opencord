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
import os
# from logging.handlers import RotatingFileHandler 

# Versioning 
# Major.Minor.Revision (bug fixes, small updates).build number


# Known bugs: 't or anything with ' will break the input and the server. 

# Encryption: 
"""
    - Client generates an asymmetric keypair. 
    - Client sends public key with initial authentication request to server 
    - Server uses the key to encrypt the response and sends back the response to the client
    - If the client is authenticated the server generates a symmetric key and includes that key in the response to the client.  

    * Both the clients asymmetric key and servers symmetric key are "randomly" generated for each connection. 
    
"""


class Client:
    def __init__(self, client_version, profile_hash):  # Profile hash can be anything until I develop a hashing method
        self.client_version = client_version  # The client version
        self.phash = profile_hash  # Just going to be a name or something
        self.connected = datetime.now()
        self.messages = {}
        self.token = None  # Need to implement a token
        self.client_key = None  # Clients public key
        self.private_key = None  # The servers private key (or key for this session)
        self.symmetric_key = None  # Once encryption is established the server generates a symmetric key
        self.data = None
        self.id = None
        self.last_message = None

    def read_message(self, message):
        message = json.loads(message)
        t = message.pop('token')
        n = message.pop('n')

        self.messages[n] = message
        client = Client("0.0.0.1", self.data)
        # return message['content']
        return message

        """
        Build a new message 
        - Content: message content 
        - Type: message type (0 normal, 1 Notice, 2 Warning, 3 Error)
        - m_time: time of message
        - m_from: who the message is from
        - message_id: id of the message
        """

    def build_server_message(self, room_name, param):
        pass


class Server:
    def __init__(self):
        self.messages = None
        self.connections = []
        self.active_connections = []
        self.active_users = []
        self.server_version = "0.0.0.1"
        self.server_hash = None  # Need to implement unique server hashes (easy way for server identification)
        self.verification_hash = None  # Need to implement unique verification hashes for the server
        self.database = oc_database.Database()

    # Authorize access to the server 
    def authorize(self, user):
        message = {"version": self.server_version, "token": None}  # holds the auth message
        return message

    def save_messages(self, sent, user):
        if user in self.messages.keys():
            self.messages[user] = {**self.messages[user], **sent}

        else:
            self.messages[user] = sent

    def load_messages(self, user):
        if user not in self.messages.keys():
            return 1

        long_string = ">>>  "  # Combine all messages into 1 long string (for now )
        user_messages = self.messages[user]
        for message in user_messages.keys():
            long_string += user_messages[message]['content'] + "\n" + ">>>  "

        return long_string

    # 0: normal message, 1: update (update messages), 2:image, 3: info(switch server, add user, etc.),
    def build_message(self, content=None, m_type=0, m_time=None, m_from=None, message_id=None, message_room=None):
        message = {"content": content, "type": m_type, "time": m_time, "from": m_from, "id": message_id,
                   "room": message_room}

        return message

    def build_message_file(self, content=None, m_type=2, m_from=None, file_type=None):
        message = {"content": content, "type": m_type, "from": m_from, "file_type": file_type}

        return message

    # Type 3 is server message (alert)
    # Type 4
    def build_server_message(self, content=None, type=3):
        message = {"type": type, "content": content, }

        return message


opencord_server = Server()


def update(timeout=1):
    while_counter = 0
    time.sleep(timeout)
    # message = bytes("Testing update", 'utf-8')
    while True:
        # print(f"active connections: {len(opencord_server.active_connections)}")
        # print(f"Active connections: {opencord_server.active_connections}")
        for i in opencord_server.active_connections:
            for client, connection in i.items():
                master_string = ""
                # print(f"Client: {client.phash}")
                # print(f"Connection: {connection}")

                # TODO: Merge these into 1 query 
                room = opencord_server.database.sanitized_query("SELECT room FROM user WHERE name =?", [client.phash])
                room = room.fetchone()
                # print(f"Room: {room}")

                conversation = opencord_server.database.sanitized_query("SELECT conv_id FROM user WHERE name =?",
                                                                        [client.phash])
                conversation = conversation.fetchone()
                # print(f"Conversation: {conversation}")

                # room = opencord_server.database.query(f"SELECT room FROM user WHERE name = '{client.phash}'")

                if room is not None:
                    room = room[0]

                if conversation is not None:
                    conversation = conversation[0]

                if room is not None:
                    # print(f"Room: {room}")
                    messages = opencord_server.database.sanitized_query(
                        "SELECT * FROM message WHERE room_id =? ORDER BY id DESC LIMIT 10", [room])
                    # messages = opencord_server.database.query
                    # (f"SELECT * FROM message WHERE room_id = {room} ORDER BY id DESC LIMIT 10")
                    messages = messages.fetchall()
                    # print(f"Messages: {messages}")
                    # ic(len(messages))
                    # print(f"Last message: {messages[0][0]}")
                    message_bundle = {}
                    if client.last_message is None:
                        try:
                            client.last_message = messages[0][0]
                        except (IndexError, TypeError) as e:
                            # Error with index being out of range for messages[0][0] meaning no messages in the room. 
                            client.last_message = None
                        for i, m in enumerate(messages):
                            try:

                                name = opencord_server.database.sanitized_query("SELECT name FROM user WHERE id =?",
                                                                                [m[5]])
                                # name = opencord_server.database.query(f"SELECT name FROM user WHERE id = {m[5]}")
                                name = name.fetchone()[0]
                                # print(f"message_id: {m[0]}")

                                # print(f"Message: {m[2]}")
                                # print(f"Message: {m}")

                                room_name_cursor = opencord_server.database.sanitized_query("SELECT name FROM room WHERE id =?", [m[4]])
                                room_name = room_name_cursor.fetchone()[0]

                                built_message = opencord_server.build_message(content=m[2], m_time=m[1], m_from=name,
                                                                              message_id=m[0], message_room=room_name)
                                message_bundle[i] = built_message
                                # print(f"Bundle: {message_bundle}")
                                master_string = f"{name}: {m[2]}\n" + master_string
                                # print(master_string)
                            except Exception as e:
                                print(f"Last message Error: {e}")
                                print(f"Last meassage: {client.last_message}\n Room: {room}")

                        # message = bytes(master_string, 'utf-8')
                        message = json.dumps(message_bundle).encode('utf-8')
                        connection.sendall(message)

                    elif client.last_message < messages[0][0]:
                        message_bundle = {}
                        print(f"Elif here")
                        try:
                            for x in range(0, messages[0][0] - client.last_message):
                                # print(f"index: {x}")
                                message_text = messages[x][2]
                                # print(f"Message id: {message_id}")
                                try:
                                    name = opencord_server.database.sanitized_query("SELECT name FROM user WHERE id =?",
                                                                                    [messages[x][5]])
                                    # name = opencord_server.database.query
                                    # (f"SELECT name FROM user WHERE id = {messages[x][5]}")
                                    name = name.fetchone()[0]
                                    master_string = f"{name}: {message_text}\n" + master_string

                                    room_name_cursor = opencord_server.database.sanitized_query("SELECT name FROM room WHERE id =?", [messages[x][4]])
                                    room_name = room_name_cursor.fetchone()[0]

                                    built_message = opencord_server.build_message(content=messages[x][2],
                                                                                m_time=messages[x][1], m_from=name,
                                                                                message_id=messages[x][0], message_room=room_name)
                                    message_bundle[x] = built_message
                                    client.last_message = messages[0][0]
                                except Exception as e:
                                    print(f"Update Error: {e}")
                                    print(f"Last meassage: {client.last_message}\n Room: {room}")

                            message = json.dumps(message_bundle).encode('utf-8')
                            connection.sendall(message)

                        except Exception as elifError: 
                            print(f"Elif Error: {elifError}")

                        # message = bytes(master_string, 'utf-8')

                if conversation is not None:
                    messages = opencord_server.database.sanitized_query(
                        "SELECT * FROM chat WHERE conv_id =? ORDER BY id DESC LIMIT 10", [conversation])
                    # messages = opencord_server.database.query
                    # (f"SELECT * FROM message WHERE room_id = {room} ORDER BY id DESC LIMIT 10")
                    messages = messages.fetchall()
                    print(f"Messages 2: {messages}")
                    # ic(len(messages))

                    if client.last_message is None:
                        try:
                            client.last_message = messages[0][0]
                        except (IndexError, TypeError) as e:
                            # Error with index being out of range for messages[0][0] meaning no messages in the room. 
                            client.last_message = None
                        for m in messages:
                            # ic(m)
                            try:
                                user = opencord_server.database.sanitized_query(
                                    "SELECT user_id FROM members WHERE id =?", [m[5]])
                                user = user.fetchone()[0]

                                user = opencord_server.database.sanitized_query("SELECT name FROM user WHERE id =?",
                                                                                [user])
                                print(f"user: {user}")
                                user = user.fetchone()[0]
                                # ic(user)

                                # member = opencord_server.database.sanitizedQuery
                                # ("SELECT member_id FROM chat WHERE id =?", [m[5]])
                                # member = opencord_server.database.sanitizedQuery
                                # ("SELECT id FROM members WHERE user_id =? AND conv_id =?", [m[], conversation])
                                # member = member.fetchone()[0]
                                # name = opencord_server.database.sanitizedQuery
                                # ("SELECT user_id from members WHERE id =?", [m])
                                # name = name.fetchone()[0]
                                # ic(name)

                                # print(f"Message: {m[2]}")
                                master_string = f"{user}: {m[2]}\n" + master_string
                                # print(master_string)
                            except Exception as e:
                                print(f"Last conversation message Error: {e}")
                                print(f"Last conversation meassage: {client.last_message}\n Room: {room}")

                        message = bytes(master_string, 'utf-8')
                        connection.sendall(message)

                    elif client.last_message < messages[0][0]:
                        print("conversation found no messages")
                        for x in range(0, messages[0][0] - client.last_message):
                            # print(f"index: {x}")
                            message_text = messages[x][2]
                            m = messages[x]
                            # ic(m)
                            # print(f"Message id: {message_id}")
                            try:
                                # member = opencord_server.database.sanitizedQuery
                                # ("SELECT id FROM members WHERE user_id =? AND conv_id =?", [client.id, conversation])
                                # member = member.fetchone()[0]
                                # name = opencord_server.database.sanitizedQuery
                                # ("SELECT user_id from members WHERE id =?", [member])
                                # name = name.fetchone()[0]
                                user = opencord_server.database.sanitized_query(
                                    "SELECT user_id FROM members WHERE id =?", [m[5]])
                                user = user.fetchone()[0]
                                user = opencord_server.database.sanitized_query("SELECT name FROM user WHERE id =?",
                                                                                [user])
                                user = user.fetchone()[0]

                                master_string = f"{user}: {message_text}\n" + master_string

                                client.last_message = messages[0][0]
                            except Exception as e:
                                print(f"Update conversation Error: {e}")
                                print(f"Last conversation meassage: {client.last_message}\n Room: {room}")

                        # ic(master_string)
                        message = bytes(master_string, 'utf-8')
                        connection.sendall(message)


                    # Update the channel list
                    # Update the Currently connected users list 
                    # Update the conversations (the number of conversations and the users)

                if (while_counter ==  0 or while_counter % 5 == 0):
                    rooms_list = []
                    result = opencord_server.database.query("SELECT name FROM room")
                    result = result.fetchall()
                    try:
                        # print(f"Result: {result}") 
                        for r in result:
                            rooms_list.append(r[0])
                    except Exception as e:
                        pass
                        

                    # connected_users = []
                    all_users = []
                    user_d = {}

                    # print(f"Connections: {opencord_server.connections}")
                    # print(f"Active Connections: {opencord_server.active_connections}")
                    for person in opencord_server.active_connections: 

                        u_name = list(person.keys())[0].phash
                        u_id = list(person.keys())[0].id
                        user_d[u_id] = u_name

                    for person in opencord_server.connections: 
                        all_users.append(person.phash)
                        # print(f"Person3: {person.phash}")
                    
                    update_packet = {
                        "type":3, 
                        "connected": user_d, 
                        "rooms": rooms_list, 
                    }

                    msg = json.dumps(update_packet).encode('utf-8')
                    # print(f"While Counter: {while_counter}")
                    

                    connection.sendall(msg)
        
        
        
        while_counter += 1
        time.sleep(timeout)


class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"Client address: {self.client_address}")
        logger.info(f"New connection established: {self.client_address}")
        print(f"Request: {self.request}")
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self.data}")
        print(f"Client init packet: {self.data}")
        self.request.sendall(self.data.upper())

        while True:
            print(f"Socket: {server.socket._closed}")
            # self.data = self.request.recv(1024).strip()
            self.data = self.request.recv(1024)
            if not self.data:
                print("Client Disconnected (tcpHandler)")
                logger.info(f"Client Disconnected: {self.client_address}")
                # remove client from the list of active connections
                break

            # print(f"Stripped data: {self.data.strip()}")
            message = self.data.strip()
            print(f"Message: {message}")
            message = message.decode('utf-8')
            new_message = "Server says: " + message.upper() + '\n'
            new_message = bytes(new_message, 'utf-8')

            print(f"{self.client_address[0]} wrote: {message}")
            self.request.sendall(new_message)


class ThreadedTCPHandler(socketserver.BaseRequestHandler):

    # # Parse the message (might need in the future but for now regex)
    @staticmethod
    def parse_message(message):
        parsed_message = re.search('^\?>', message)
        return

        # Replaces self.request.sendall() and builds the packet so it can be fully received

    def senda(self, message):
        msg_size = sys.getsizeof(message)

        # If the message size is larger than 1024 bytes prep with a size packet.
        if msg_size > 1024:
            msg = {"size": msg_size}
            msg = json.dumps(msg).encode('utf-8')
            self.request.sendall(msg)

        # msg = json.dumps(msg).encode('utf-8')
        msg = bytes(message, 'utf-8')
        # msg = msg_size + msg
        self.request.sendall(msg)

    def handle(self):

        self.data = self.request.recv(1024).strip()
        message = self.data.strip()
        message = self.data.decode('utf-8')
        msg_object = json.loads(message)
        print(f"{self.client_address[0]} wrote: {self.data}")

        client = Client("0.0.0.1", msg_object['profile'])

        opencord_server.connections.append(client)  # Add client to the list of current connections
        # query = "SELECT 1 FROM user where name = " + msg_object['profile']
        # check_user = opencord_server.database.query(query) # Check if user exists in the database

        # IF the user is not in the database add them into the database
        if opencord_server.database.check_user(msg_object['profile']) == 0:
            opencord_server.database.insert_user(msg_object['profile'])  # Add user to the database
            logger.info(f"New client: {msg_object['profile']}")
            welcome = f"""
                Welcome {client.phash}!
                Join a room using the /join roomname (replacing roomname with the room you want to join) command.
                For more commands enter /help or /? to view the full list of commands.
            """
            new_message = bytes(welcome, 'utf-8')
            self.request.sendall(new_message)
            user_id = opencord_server.database.sanitized_query("SELECT id FROM user WHERE name = ?", [client.phash])
            # user_id = opencord_server.database.query(f"SELECT id FROM user WHERE name = '{client.phash}'") 
            user_id = user_id.fetchone()[0]
            client.id = user_id

            # update the users status to online
            opencord_server.database.set_user_status(client.phash, 1)
            print(f"Client {client.phash} is online.")

        else:
            try:
                logger.info(f"Client connected: {msg_object['profile']}")

                user_id = opencord_server.database.sanitized_query("SELECT id FROM user WHERE name = ?", [client.phash])
                # user_id = opencord_server.database.query(f"SELECT id FROM user WHERE name = '{client.phash}'") 
                user_id = user_id.fetchone()[0]
                client.id = user_id

                # update the users status to online
                opencord_server.database.set_user_status(client.phash, 1)
                print(f"Client {client.phash} is online.")

                room_id = opencord_server.database.sanitized_query("SELECT room FROM user WHERE id =?", [client.id])
                # room_id = opencord_server.database.query(f"SELECT room FROM user WHERE id = {client.id}")
                room_id = room_id.fetchone()[0]
                # ic(room_id)
                if room_id is not None:
                    logger.info(f"{msg_object['profile']} is in {room_id}")
                    room_name = opencord_server.database.sanitized_query("SELECT name FROM room WHERE id =?", [room_id])
                    # room_name = opencord_server.database.query(f"SELECT name FROM room WHERE id = {room_id}")
                    room_name = room_name.fetchone()[0]
                    client.build_server_message(room_name, 3)
                    welcome = f"""
                    You have joined {room_name}
                    """ + "\n"
                else:
                    logger.info(f"{msg_object['profile']} is not in a room.")
                    welcome = f"""
                    Welcome {client.phash}!
                    Join a room using the /join roomname (replacing roomname with the room you want to join) command.
                    For more commands enter /help or /? to view the full list of commands.
                    """

            except Exception as e:
                print(f"Welcome Error: {e}")
                welcome = f"""
                    Welcome {client.phash}!
                    Join a room using the /join roomname (replacing roomname with the room you want to join) command.
                    For more commands enter /help or /? to view the full list of commands.
                    """
                logger.error(f"Welcome Error: {e}")

            new_message = bytes(welcome, 'utf-8')
            self.request.sendall(new_message)

        print(f"Client address: {self.client_address}")
        print(f"Request: {self.request}")

        object_identifier = {client: self.request}
        opencord_server.active_connections.append(object_identifier)
        # opencord_server.active_users.append()
        # self.data = self.request.recv(1024).strip()
        cur_thread = threading.current_thread()
        print(f"Thread: {cur_thread}")

        # print(f"{self.client_address[0]} wrote: {self.data}")
        # self.request.sendall(self.data.upper())
        # loaded_messages = opencord_server.load_messages(client.phash)
        # if loaded_messages != 1:
        #     self.request.sendall(bytes(loaded_messages, 'utf-8'))

        while True:
            try:
                # print(f"Socket: {server.socket._closed}")
                # self.data = self.request.recv(1024).strip()
                self.data = self.request.recv(1024)
                if not self.data:
                    print("Client Disconnected (while)")
                    opencord_server.database.set_user_status(client.phash, 0)
                    opencord_server.active_connections.remove(object_identifier)

                    logger.warning(f"{client.phash} disconnected.")
                    # opencord_server.save_messages(client.messages, client.phash)
                    break

                # print(f"Stripped data: {self.data.strip()}")
                message = self.data.strip()
                # message = message.decode('ascii') 
                m = client.read_message(message)
                if m['type'] == 'file':
                    print(f"m: {m}")
                    name = m['name']

                    size = m['size']
                    print(f"Prep to receive: {size}")
                    print(0)
                    # with open("test.jpg", "wb") as f:
                    with open(name, "wb") as f:
                        # f.write(file)
                        while size > 0:
                            file = self.request.recv(1024)
                            f.write(file)
                            size -= 1024
                    m = "/file"
                    # print(f"File: {file.strip()}") 
                else:
                    m = m['content']
                    # print(f"Message: {message}")
                    m = str(m)

                # x = re.search('^\S+', m)
                # x = re.search("^\?>", m)
                # print(f"X: {x}")
                # logger.info(f"{client.phash} says {m}")
                if re.search("^\/", str(m)):

                    # Parse the command it will remove the ?> and the spaces until it hits the actual command
                    parsed_command = re.sub(r'^\/', '', m)  # Removes the starting slash from the command
                    parsed_command = re.sub(r"^\s+", '',
                                            parsed_command)  # Removes white spaces from the start of the command
                    # quoted_command = re.findall(r'"(?:\\"|.)*?"', m) # Finds all the quoted items in the command
                    # parsed_command = re.split("\s", parsed_command) # Splits the command word by word
                    regex = r"""("[^"]*"|'[^']*'|[\S]+)+"""  # Seperates the command by word and by quoted items
                    parsed_command = re.findall(regex, parsed_command)

                    print(f"parsed command: {parsed_command}")

                    # Python switch statement 
                    new_message = None
                    logger.info(f"{client.phash} parsed command: {parsed_command}")
                    match parsed_command[0]:
                        case "users":
                            headers = ["Users"]
                            # get all users with a status of 1 (online)
                            current_connected_users = opencord_server.database.sanitized_query(
                                "SELECT name FROM user WHERE status =?", [1])

                            current_connected_users = current_connected_users.fetchall()
                            for i, user in enumerate(current_connected_users):
                                if user[0] == client.phash:
                                    current_connected_users[i] = [f"{user[0]} (you)"]
                            pretty_format = tabulate(current_connected_users, headers, tablefmt="grid") + "\n"
                            new_message = bytes(pretty_format, 'utf-8')
                            self.request.sendall(new_message)
                            logger.info(f"{client.phash} uses users command.")

                        case "rooms":
                            result = opencord_server.database.query("SELECT name FROM room")
                            result = result.fetchall()
                            table = []
                            headers = ["Rooms"]
                            for room in result:
                                table.append([room[0]])

                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"
                            # print(f"Result from query: {result}")
                            new_message = bytes(pretty_format, 'utf-8')
                            self.request.sendall(new_message)
                            logger.info(f"{client.phash} uses rooms command.")

                        case "join":
                            room_id = opencord_server.database.sanitized_query("SELECT id FROM room WHERE name =?",
                                                                               [parsed_command[1]])
                            # room_id = opencord_server.database.query
                            # (f"SELECT id FROM room WHERE name = '{parsed_command[1]}'")
                            room_id = room_id.fetchone()[0]
                            # print(f"Room ID: {room_id}")

                            # Make 1 query 
                            opencord_server.database.sanitized_query("UPDATE user SET room =? WHERE name =?",
                                                                     [room_id, client.phash])
                            opencord_server.database.sanitized_query("UPDATE user SET conv_id =? WHERE name =?",
                                                                     [None, client.phash])
                            # opencord_server.database.query
                            # (f"UPDATE user SET room = {room_id} WHERE name = '{client.phash}'")
                            client.last_message = None

                            new_message = bytes(f"You have joined {parsed_command[1]}\n", 'utf-8')
                            self.request.sendall(new_message)
                            logger.info(f"{client.phash} uses join command and joins {room_id}.")

                        case "createroom":
                            opencord_server.database.sanitized_query("INSERT INTO room (name) VALUES (?)",
                                                                     [parsed_command[1]])
                            # opencord_server.database.query(f"INSERT INTO room (name) VALUES ('{parsed_command[1]}')")
                            new_message = bytes(f"Room {parsed_command[1]} created.\n", 'utf-8')
                            self.request.sendall(new_message)
                            logger.info(f"{client.phash} uses createroom command and creates {parsed_command[1]}.")

                        case "help":
                            headers = ["Command", "Description"]
                            table = [
                                ["/users", "List the servers users."],
                                ["/rooms", "List the rooms in the server."],
                                ["/join RoomName", "Join a room in the server."],
                                ["/createroom RoomName", "Create a new room in the server."],
                                ["/conversations", "List the conversations that you are in."],
                                ['/pm targetuser "Message that you want to send"', 'Private Message another user.'],
                                ["/help or /?", "Lists the commands available in the server."],
                                ["/exit", "Exit the server (terminates the connection with the server)."]
                            ]

                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"
                            # new_message = bytes(pretty_format, 'utf-8') 
                            # self.request.sendall(new_message)
                            self.senda(pretty_format)
                            logger.info(f"{client.phash} uses help command.")

                        case "pm":
                            if len(parsed_command) == 3:
                                to_user = parsed_command[1]
                                msg = parsed_command[2]
                                msg = msg.strip('\"')  # Remove the quotes
                                to_user = to_user.strip('\"')
                                # print(f"To: {to_user}")
                                # print(f"Message: {msg}")

                                # Begin the conversation which essentially creates a room (conversation)
                                opencord_server.database.sanitized_query("INSERT INTO conversation (owner) VALUES(?)",
                                                                         [client.id])
                                conversation = opencord_server.database.sanitized_query(
                                    "SELECT * FROM conversation WHERE owner =? ORDER BY id DESC LIMIT 1", [client.id])
                                conversation = conversation.fetchone()
                                # print(f"Conversation: {conversation.fetchall()}")
                                conversation_id = conversation[0]
                                print(f"Conversation ID: {conversation_id}")
                                logger.info(f"{client.phash} uses pm command.")

                                try:
                                    member_id = opencord_server.database.sanitized_query(
                                        "SELECT * FROM user WHERE name =?", [to_user])
                                    member_id = member_id.fetchone()[0]
                                    # print(f"Member_id: {member_id}")

                                    # This will probably end up being a loop eventually. 
                                    opencord_server.database.sanitized_query(
                                        "INSERT INTO members (user_id, conv_id) VALUES(?, ?)",
                                        [member_id, conversation_id])
                                    opencord_server.database.sanitized_query(
                                        "INSERT INTO members (user_id, conv_id) VALUES(?, ?)",
                                        [client.id, conversation_id])

                                    # This might just be for testing the backend. We don't really care about the
                                    # current conversation a user is or isn't in (may be involved in multiple at once)
                                    print(f"start conversation: {conversation_id}")
                                    # opencord_server.database.sanitizedQuery("INSERT INTO user (conv_id) VALUES(?)",
                                    # [conversation_id])

                                    # When you pm someone you leave your current room and join a conversation room
                                    # opencord_server.database.sanitizedQuery("INSERT INTO user (room,
                                    # conv_id) VALUES(?, ?)", [None, conversation_id])
                                    opencord_server.database.sanitized_query(
                                        "UPDATE user SET room =?, conv_id =? WHERE id =?",
                                        [None, conversation_id, client.id])
                                    # query_conv = opencord_server.database.sanitizedQuery("SELECT conv_id FROM user
                                    # WHERE name =?", [client.phash]) print(f"Query conv: {query_conv.fetchall()}")

                                    new_message = f"New conversation started with {to_user}.\n\n"
                                    new_message = bytes(new_message, 'utf-8')
                                    self.request.sendall(new_message)

                                    new_message = bytes(f"{client.phash}: {msg}" + "\n", 'utf-8')
                                    self.request.sendall(new_message)
                                    client.last_message = None

                                except Exception as f:
                                    print(f"Probably invalid user name")
                                    logger.error(f"Error: {f}")
                                    print(f)

                        case "joinconv":
                            conv_id = parsed_command[1]  # What conversation to join 
                            conversations = opencord_server.database.sanitized_query(
                                "SELECT * FROM members WHERE user_id =?", [client.id])
                            conversations = conversations.fetchall()

                            # Test if there are no conversations and output no conversations to join 
                            join_conv = None  # Gets set when we find the conversation in the list of conversations if it is None after search throw error
                            for conv in conversations:
                                # ic(conv)
                                # ic(conv[1])
                                if conv[1] == int(conv_id):
                                    join_conv = conv_id
                                    break

                            logger.info(f"{client.phash} uses joinconv command to join conversation {conv_id}")
                            if join_conv is None:
                                print(f"Error conversation with id {conv_id} not found. ")
                                logger.error(f"Error: conversation {conv_id} not found.")

                            # Combine these two queries into 1 query 
                            opencord_server.database.sanitized_query("UPDATE user SET conv_id =? WHERE name =?",
                                                                     [join_conv, client.phash])
                            opencord_server.database.sanitized_query("UPDATE user SET room =? WHERE name =?",
                                                                     [None, client.phash])

                            new_message = bytes(f"You have joined conversation {parsed_command[1]}\n", 'utf-8')
                            self.request.sendall(new_message)
                            client.last_message = None

                        case "conversations":

                            result = opencord_server.database.sanitized_query("SELECT * FROM members WHERE user_id =?",
                                                                              [client.id])
                            result = result.fetchall()

                            logger.info(f"{client.phash} uses conversations command.")

                            table = []
                            members_list = []
                            for x in result:
                                # ic(x)
                                members = opencord_server.database.sanitized_query(
                                    "SELECT * FROM members WHERE conv_id =?", [x[1]])
                                members_list.append(members.fetchall())

                            for room in result:
                                table.append([room[1]])

                            for x in range(0, len(members_list)):
                                member_string = ""
                                for y in members_list[x]:
                                    name = opencord_server.database.sanitized_query("SELECT name FROM user WHERE id =?",
                                                                                    [y[2]])
                                    name = name.fetchone()[0]
                                    # print(f"Name: {name}")
                                    member_string += name + ", "
                                member_string = member_string.strip(', ')
                                table[x].append(member_string)

                            # print(f"Members_list: {members_list}")
                            # print(f"Result: {result}")
                            # conversations = [] 
                            # for x in result[1]:
                            #     conversations.append(x[1])
                            # print(f"Member results: {result}")
                            headers = ["Conversation ID", "Members"]

                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"
                            # print(f"Result from query: {result}")
                            new_message = bytes(pretty_format, 'utf-8')
                            self.request.sendall(new_message)

                        case "?":
                            headers = ["Command", "Description"]
                            table = [
                                ["/users", "List the currently connected users."],
                                ["/rooms", "List the rooms in the server."],
                                ["/join RoomName",
                                 "Join a room in the server (no spaces allowed in room name for now)."],
                                ["/createroom RoomName",
                                 "Create a new room in the server (no spaces allowed in room name for now)."],
                                ["/help or /?", "Lists the commands available in the server."],
                                ["/exit", "Exit the server (terminates the connection with the server)."]
                            ]

                            logger.info(f"{client.phash} uses ? command.")

                            pretty_format = tabulate(table, headers, tablefmt="grid") + "\n"
                            # new_message = bytes(pretty_format, 'utf-8') 
                            # self.request.sendall(new_message)
                            self.senda(pretty_format)

                        # Used to test sending different things from the server to the client
                        case "st":
                            header = """\033[91m
                                        ·································································
                                        : _____                                                  __     :
                                        :/\  __`\                                               /\ \    :
                                        :\ \ \/\ \  _____      __    ___     ___    ___   _ __  \_\ \   :
                                        : \ \ \ \ \/\ '__`\  /'__`\/' _ `\  /'___\ / __`\/\`'__\/'_` \  :
                                        :  \ \ \_\ \ \ \L\ \/\  __//\ \/\ \/\ \__//\ \L\ \ \ \//\ \L\ \ :
                                        :   \ \_____\ \ ,__/\ \____\ \_\ \_\ \____\ \____/\ \_\\ \___,_\:
                                        :    \/_____/\ \ \/  \/____/\/_/\/_/\/____/\/___/  \/_/ \/__,_ /:
                                        :             \ \_\                                             :
                                        :              \/_/                                             :
                                        ·································································
                                        """ + "\u001b[0m" + '\n'
                            print(f"Header size: {sys.getsizeof(header)}")
                            self.senda(header)

                        case _:
                            # new_message = "Server says: " + m.upper() + '\n'
                            print(f"Default case")
                            logger.warn(f"{client.phash} invalid command/command not found.")
                            new_message = "Default case \n"
                            new_message = bytes(new_message, 'utf-8')
                            self.request.sendall(new_message)

                            # print(f"{self.client_address[0]}: {message}")
                else:
                    # new_message = f"{client.phash}: {m}"
                    room = opencord_server.database.sanitized_query("SELECT room FROM user WHERE id =?", [client.id])
                    room = room.fetchone()
                    # ic(room)
                    conversation = opencord_server.database.sanitized_query("SELECT conv_id FROM user WHERE id =?",
                                                                            [client.id])
                    conversation = conversation.fetchone()
                    # room = opencord_server.database.query(f"SELECT room FROM user WHERE id = '{client.id}'")
                    # ic(room_id)
                    # print(f"Room: {room.fetchone()[0]}")
                    # print(f"Room: {room.fetchone()[0]}")
                    # ic(room.fetchone())
                    # ic(room)
                    # ic(conversation)
                    # conversation = None

                    # print(f"Room: {room}")
                    # Sometimes it returns None sometimes (None, ) IDK 
                    if room is not None:
                        room = room[0]

                    if conversation is not None:
                        conversation = conversation[0]

                    print(f"room: {room}")
                    if room is not None:
                        opencord_server.database.sanitized_query(
                            "INSERT INTO message (text, room_id, user_id) VALUES (?, ?, ?)", [m, room, client.id])
                        # opencord_server.database.query(f"INSERT INTO message (text, room_id, user_id) VALUES ('{
                        # m}', {room}, {client.id})")

                    elif conversation is not None:
                        # ic(client.id)
                        # ic(conversation)
                        member = opencord_server.database.sanitized_query(
                            "SELECT id FROM members WHERE user_id =? AND conv_id =?", [client.id, conversation])
                        member = member.fetchone()[0]
                        # ic(member)
                        opencord_server.database.sanitized_query(
                            "INSERT INTO chat (text, conv_id, member_id) VALUES (?, ?, ?)", [m, conversation, member])

                    else:
                        print(f"Room nor conversation is found")
                        new_message = bytes("Error: You need to join a room or conversation to chat.\n", 'utf-8')
                        self.request.sendall(new_message)
                        logger.error(f"No room or conversation found for {client.id}.")

                    # new_message = bytes(m, 'utf-8')
                    # self.request.sendall(new_message)

            except Exception as e:
                print(f"Switch Error: {e}")
                try:
                    opencord_server.active_connections.remove(object_identifier)
                except Exception as c:
                    # for identifier in opencord_server.active_connections 
                    print(f"Error: {c}")
                    break
                logger.error(f"Switch Error: {e}")
                # opencord_server.save_messages(client.messages, client.phash)
                # new_message = bytes("Error: You need to join a room to chat.\n", 'utf-8')
                # self.request.sendall(new_message)
                # break


# The class should already be defined but we can override functions inside the class
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    print("Called threadedTCPServer")
    pass


if __name__ == '__main__':
    # HOST, PORT = "10.200.0.224", 9090
    HOST, PORT = "localhost", 9090

    # logging.basicConfig(level=logging.INFO, filename="logfile.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    loghandler = logging.FileHandler(filename="logfile.log")
    loghandler.setFormatter(formatter)
    logger.addHandler(loghandler)
    logger.info("Starting Server")

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

        # update_thread = threading.Thread(target=server

        # The entire Python program exits when only daemon threads are left.
        # So they are abruptly stopped at shutdown meaning resources may not be released properly. 
        # For threads to stop gracefully, they should be non-daemonic and use a signalling mechanism
        # such as an Event.
        server_thread.daemon = True
        # server_thread_udp.daemon = True

        server_thread.start()
        # server_thread_udp.start()

        # If we want the server to control the updating we use this
        update_thread = threading.Thread(target=update, daemon=True)  # This is the update Thread
        update_thread.start()

        print(f"Server loop running in thread {server_thread.name}")
        # print(f"UDP server loop running in thread {server_thread_udp.name}")
        # print(f"Server UDP loop running in thread {server_thread_udp.name}")
        print(f"Server running on port {PORT}")
        while True:
            try:
                t = input("\"exit\" to stop the server: ")
                if t.strip().lower() == "exit":
                    print("Beginning shutdown")
                    for s in opencord_server.active_connections:
                        key = list(s.keys())[0]
                        sock = s[key]
                        sock.close()
                    server.shutdown()
                    # unbind the socket
                    server.server_close()

                    break

            except Exception as e:
                for x in opencord_server.active_connections:
                    print(f"X: {x}")
                print(f"Error Here: {e}")
                break
        print("Stopping server")
        logger.info("Stopping Server")
        server.shutdown()
        # unbind the socket
        server.server_close()
        # update_thread.stop()
