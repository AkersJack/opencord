# Opencord

An opensource Discord clone


## Installation
In order to build: 
    1. Install NPM (https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi)

    2. In terminal/cmd of the working directory enter the command: npm install 

    3. To start the application in terminal/cmd enter the command: npm start


To ensure all modules/libraries are the same version create a Python virtual environment with this command in your cmd/terminal: 

    python -m venv /path/to/new/virtual/environment


To activate the virtual environment on Windows in PowerShell/cmd enter the command: 
    <venv>\Scripts\activate

To activate the virtual environment on Mac in the terminal enter: 
    source venv/bin/activate

Once activated to the far left in your terminal/cmd it should have the name of the virtual environment. 

To install the required libraries/modules in the venv enter the command: 

    pip install -r requirements.txt 


requirements.txt is included in the git files. 


To run Flask server:
    While in the webserver directory in terminal/cmd enter the command:

    flask --app main run

To access the web server pages in a browser go to the URL: 

    http://127.0.0.1:5000


# How to test/run locally
   - Start by running the server.py, leaving it open in a separate terminal
      - `$ python3 server.py`
   - Then run client.py to create a user for yourself.
      - `$ python3 client.py`
   - Now we need to open the electron client.
      - `$ npm init`
      - `$ npm start`
   - Commands to the server can be entered through the text box.
      - enter `/help` to see the list of commands in the terminal.


# Opencord Server 

- The Opencord server runs by default on port 9090 (can be changed in code). 
- To exit/close the server enter the command "exit". To exit all connections to the server must be closed (it is kind of "buggy" so you might need to enter the command twice).  
 
## FFMPEG
- Required (https://ffmpeg.org/download.html)


# Opencord Client
- Takes 1 argument which is the username for the client. The username can't have any spaces in it. 
- Room names can't have any spaces in them. 
- /help or /? brings up the command list. 
- /exit closes the client and terminates the connection with the server. 

## Currently You can: 
- Create rooms.
- List users who are currently online. 
- Join rooms.
- Chat with others in the room. 


