'''
This file is going to handle everything regarding the database
'''
import sqlite3
import json
import os
from tabulate import tabulate


class Database:
    def __init__(self) -> None:
        self.location = "./outputs/opencord_database.db"  # Location of the database
        self.cur = None  # Database cursor (needed to execute SQL queries)
        self.con = None  # Database connection
        self.connect_to_database()

    # If the database didn't exist create all the tables. 
    def build_database(self) -> None:
        # Enable foreign keys
        self.query("PRAGMA foreign_keys = ON")

        # Create the user table
        self.cur.execute(open("../scripts/create_user_table.sql", "r").read())

        # Room table  
        self.cur.execute(open("../scripts/create_room_table.sql", "r").read())

        # Messages table 
        self.cur.execute(open("../scripts/create_messages_table.sql", "r").read())

        # Conversation table (stores conversations)
        self.cur.execute(open("../scripts/create_conversation_table.sql", "r").read())

        # chat table (stores conversation chat messages)
        self.cur.execute(open("../scripts/create_chat_table.sql", "r").read())

        # Stores the members of the conversation (could probably just use users table)
        self.cur.execute(open("../scripts/create_members_table.sql", "r").read())

        tables = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        print(tabulate(tables.fetchall(), headers=["Tables"]))
        print("------------\n")

    # States whether the user is online or not using a boolean value of 1 or 0
    def set_user_status(self, user, status):
        self.sanitized_query("UPDATE user SET status = ? WHERE name = ?", [status, user])

    def check_user(self, user):
        """
        Check if the user exists in the database
        @param user: The user to check
        @return: True if the user exists, False if the user doesn't exist
        """
        sql = f"""
        SELECT
            CASE
            WHEN EXISTS (
                SELECT 1
                FROM user
                WHERE name = '{user}'
            )
            THEN 1
            ELSE 0
            END AS value_exists;
        """

        response = self.sanitized_query(
            "SELECT CASE WHEN EXISTS (SELECT 1 FROM user WHERE name =?) THEN 1 ELSE 0 END AS value_exists", [user])
        return response.fetchone()[0]

    def insert_user(self, user) -> None:
        """
        Insert a user into the database
        @param user: The user to insert, should be a tuple
        @return: None
        """
        self.sanitized_query("INSERT INTO user (name) VALUES (?)", [user])

    def get_user(self, user):
        """
        Get a user from the database
        @param user: The user to get
        @return: The user
        """
        return self.sanitized_query("SELECT * FROM user WHERE name = ?", [user])

    def get_user_id(self, user):
        return self.sanitized_query("SELECT id FROM user WHERE name = ?", [user])

    def get_user_name(self, user_id):
        return self.sanitized_query("SELECT name FROM user WHERE id = ?", [user_id])

    def get_user_status(self, user):
        return self.sanitized_query("SELECT status FROM user WHERE name = ?", [user])

    def is_user_online(self, user):
        return self.sanitized_query("SELECT status FROM user WHERE name = ?", [user]) == 1

    def get_user_hash(self, user):
        return self.sanitized_query("SELECT hash FROM user WHERE name = ?", [user])

    def get_user_creation_date(self, user):
        return self.sanitized_query("SELECT creation_date FROM user WHERE name = ?", [user])

    def get_user_version(self, user):
        return self.sanitized_query("SELECT version FROM user WHERE name = ?", [user])

    # Get the users current location in the server, if they are in a room or not
    def get_user_current_room(self, user):
        return self.sanitized_query("SELECT conv_id FROM user WHERE name = ?", [user])

    def get_room_members(self, room_id):
        return self.sanitized_query("SELECT user.name FROM members JOIN user ON members.user_id = user.id WHERE "
                                    "members.room_id = ?", [room_id])

    def get_room_id(self, room_name):
        return self.sanitized_query("SELECT id FROM room WHERE name = ?", [room_name])

    def get_room_creation_date(self, room_name):
        return self.sanitized_query("SELECT creation_date FROM room WHERE name = ?", [room_name])

    def get_room_name(self, room_id):
        return self.sanitized_query("SELECT name FROM room WHERE id = ?", [room_id])

    def connect_to_database(self):
        exists = os.path.exists(self.location)
        self.con = sqlite3.connect(self.location, check_same_thread=False)
        self.cur = self.con.cursor()
        if not exists:  # If the database didn't exist create the tables
            print("DB Doesn't Exist. Creating the db...")
            self.build_database()
        return self.con

    # Load the database
    def load_database(self):
        self.con = sqlite3.connect(self.location)
        self.cur = self.con.cursor()

    def sanitized_query(self, command, parameters=None):
        command = self.cur.execute(command, parameters)
        self.con.commit()
        return command

    # Query the database
    def query(self, command):
        command = self.cur.execute(command)
        self.con.commit()
        return command
