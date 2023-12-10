'''
This file is going to handle everything regarding the database
'''
import sqlite3
import json
import os
from tabulate import tabulate


class Database:
    def __init__(self) -> None:
        self.location = "./serverdb.db"
        self.cur = None  # Database cursor (needed to execute SQL queries)
        self.con = self.connectToDatabase()  # Connection instance

    # If the database didn't exist create all the tables. 
    def buildDatabase(self) -> None:

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
        for table in tables:
            print(table)

    def checkUser(self, user):
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

        response = self.sanitizedQuery(
            "SELECT CASE WHEN EXISTS (SELECT 1 FROM user WHERE name =?) THEN 1 ELSE 0 END AS value_exists", [user])
        return response.fetchone()[0]

    def insertUser(self, user):
        self.sanitizedQuery("INSERT INTO user (name) VALUES (?)", [user])

    # Check if the database exists already and connect. If it doens't exist create the db file. 
    def connectToDatabase(self) -> None:
        exists = os.path.exists(self.location)
        self.con = sqlite3.connect(self.location, check_same_thread=False)
        self.cur = self.con.cursor()
        if not exists:  # If the database didn't exist create the tables
            print("DB Doesn't Exist. Creating the db...")
            self.buildDatabase()
        return self.con

    # Load the database
    def load_database(self):
        pass

    def sanitizedQuery(self, command, parameters=None):
        command = self.cur.execute(command, parameters)
        self.con.commit()
        return command

    # Query the database
    def query(self, command):
        command = self.cur.execute(command)
        self.con.commit()
        # print(f"Command: {command}")
        return command
