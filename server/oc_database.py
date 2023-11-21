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
        self.con = None
        self.connectToDatabase()  # Connection instance

    # If the database didn't exist create all the tables. 
    def buildDatabase(self) -> None:

        # Enable foreign keys
        self.query("PRAGMA foreign_keys = ON")

        """
        Alternative possibly cleaner method to create the tables.
        
        self.cur.executescript(open("/scripts/create_user_table.sql", "r"))
        
        """
        # Create the user table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                name VARCHAR(16),
                created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                version VARCHAR(45),
                status VARCHAR(45),
                room INTEGER,
                conv_id INTEGER,
                FOREIGN KEY (room) REFERENCES room(id),
                FOREIGN KEY (conv_id) REFERENCES conversation(id)
            )
            ''')

        # Room table  
        self.cur.execute('''CREATE TABLE IF NOT EXISTS room (
            id      INTEGER PRIMARY KEY NOT NULL, 
            created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            name    VARCHAR(45)      
           ) 
            ''')

        # Messages table 
        self.cur.execute('''CREATE TABLE IF NOT EXISTS message (
                id      INTEGER  PRIMARY KEY,
                date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                text    LONGTEXT, 
                data    LONGBLOB,  
                room_id INTEGER, 
                user_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES room(id), 
                FOREIGN KEY(user_id) REFERENCES user(id) 
            )         
            ''')
        #

        # Conversation table (stores conversations)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS conversation (
            id      INTEGER PRIMARY KEY,
            date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
            owner   INTEGER NOT NULL, 
            FOREIGN KEY(owner) REFERENCES user(id) 
            )              
            ''')

        # chat table (stores conversation chat messages)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS chat(
            id      INTEGER PRIMARY KEY, 
            date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
            text    LONGTEXT, 
            data    LONGBLOB,   
            conv_id INTEGER NOT NULL, 
            member_id INTEGER NOT NULL,
            FOREIGN KEY(conv_id) REFERENCES conversation(id), 
            FOREIGN KEY(member_id) REFERENCES members(id)
            )
            ''')

        # Stores the members of the conversation (could probably just use users table)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY,
            conv_id INTEGER NOT NULL, 
            user_id INTEGER NOT NULL,   
            FOREIGN KEY(conv_id) REFERENCES conversation(id), 
            FOREIGN KEY(user_id) REFERENCES user(id) 
            )
            ''')

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
    def load_database():
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
