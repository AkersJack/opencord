# Opencord Project

Opencord is a dynamic communication platform designed for real-time interaction. This repository contains the Opencord server and client applications' complete source code, along with the necessary scripts and utilities to set up and manage the Opencord ecosystem.

## Server
The server is built in Python and handles all backend functionalities, including user management, session control, message routing, and security. It operates on the TCP/IP protocol to ensure reliable data transmission.

### Features
- Asynchronous communication handling
- Encrypted data transfer using RSA and AES
- Room-based conversations and private messaging
- User authentication and session management
- Database integration for persisting data

## Client
The client is a lightweight interface that connects to the Opencord server, enabling users to engage in conversations, share files, and manage their profiles.

### Features
- Interactive command-line interface
- Real-time message updates
- File sharing capabilities
- User-friendly command system for room and conversation management

## Database
The system uses an SQLite database to store user data, message histories, room information, and other persistent data required for the platform's operation.

### Tables
- Users: Stores user profile information
- Rooms: Manages rooms for group conversations
- Messages: Archives messages exchanged in the rooms
- Conversations: Manages private conversations between users
- Members: Tracks members of conversations

## Installation & Setup

### Requirements
- Python 3.8 or higher
- Node.js and npm for the client interface
- FFMPEG for media handling

### Build Instructions

To set up and start using the application, follow these steps:

1. **Install Node Package Manager (NPM)**
   - Download and install NPM from the official [Node.js download page](https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi).

2. **Install Dependencies**
   - Open your terminal or command prompt.
   - Navigate to the project's working directory.
   - Run the following command to install all the necessary dependencies:
     ```sh
     npm install
     ```

3. **Start the Application**
   - In the terminal or command prompt, start the application with the command:
     ```sh
     npm start
     ```

Following these steps will install all required packages and start the Opencord application.

### Server Setup
Runs on port 9090 by default. Use "exit" to close the server; ensure all connections are terminated first.
1. Clone the repository to your local machine.
2. Navigate to the server directory.
3. Create a Python virtual environment:
```sh
python -m venv venv
```
4. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`
5. Install the required Python dependencies:
```sh
pip install -r requirements.txt
```
6. Run the server using Python:
```sh
python server.py
```

### Client Setup
Accepts a single argument for the username (no spaces allowed), Use `/help` or `/?` to view commands.
1. Navigate to the client directory.
2. Install the required npm packages:
```sh
npm install
```
3. Start the client application:
```sh
npm start
```

4. If you want to use client without the frontend:
```sh
python3 client.py <user_name>
```

### Flask Server
Run `flask --app main run` within the webserver directory. Access the web interface at `http://127.0.0.1:5000`.




