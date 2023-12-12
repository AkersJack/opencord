import * as net from 'net';
import { format } from 'date-fns';
import { createChatMessage } from './worker.js';
import * as tools from './stuff';
import * as path from 'path';
import { ipcMain, BrowserWindow} from 'electron';






const dirpath = path.resolve(__dirname, '../..')
console.log("dirpath: " + dirpath);




function checkProcessType() {
  if (process.type === 'browser') {
    console.log('Running in the main process');
  } else if (process.type === 'renderer') {
    console.log('Running in a renderer process');
  } else {
    console.log('Unknown process type');
  }
}

function sendMessageToRenderer(message: object){
  const win = BrowserWindow.getAllWindows()[0]; 
  if(win){
    win.webContents.send('from-main', message);
  }
}

// File paths 
const base_path = path.join(dirpath,  "/oc/");
const theme_path = path.join(base_path, "/themes/");
// const profile_path = path.join(base_path, "/profile/");
// const message_path = path.join(base_path, "profile/", "messages.json");
// const account_path = path.join(base_path, "profile/", "account.json");

// console.log("base_path: " + base_path);
// console.log("theme_path: " + theme_path);
// console.log("profile_path: " + profile_path);
// console.log("message_path: ", message_path);



class Communication{
    session_id: string; 
    client_version: string;
    server_version:string;
    profile_hash: string; 
    username: string; 
    messageNumber: number;
    public_key: string; 
    private_key: string;
    symmetric_key: string;
    update_packet: boolean;
    sock: unknown;
    message: unknown;
    message_path: string; 
    account_path: string;
    profile_path: string; 

    constructor(){
        this.session_id = null // ID of the chat session 
        this.client_version = "" // Version of the client
        this.server_version = "" // Version of the server
        this.profile_hash = null  // Hash of the user profile  (needs to be implemented)
        this.messageNumber = 0 // keeps track of the number of messages sent so far
        this.private_key = null // Private key (used to decrypt the servers response)
        this.public_key = null // Public key (used to encrypt the server response)
        this.symmetric_key = null // symmetric key (sent by the server and used for the rest of the session)
        this.update_packet = null // If it is an update packet or not
        this.sock = null // Socket connection
    }

    sendmsg(content:string, type = "normal", size=1024){
        const date = new Date(); 
        const formattedDate = format(date, 'yyyy-MM-dd HH:mm:ss')
        const message = JSON.stringify({
            "n": this.messageNumber,
            "time": formattedDate, 
            "content": content, 
            "token": "Need to implement", 
            "type": type, 
            "size":size, 
        });

        this.messageNumber++; 
        return message

    }

}



// const message = JSON.stringify({
//   "service":0, 
//   "client_version":"0.0.0.1", 
//   "profile":"Test", 
// });

const chat = new Communication();



ipcMain.on('message-from-renderer', (event, arg)=>{
  // IPC listener in the main process 
  console.log('Main process received message: ', arg);
  const argkeys = Object.keys(arg); 
  // console.log("Argkeys: ", argkeys);
  if(arg.hasOwnProperty('update')){
    let updateMessage = tools.readJSON(chat.message_path); 
    // console.log('Update message: ', updateMessage); 
    sendMessageToRenderer({"update":updateMessage});
  }


});






// Function to create and connect a TCP client
function startClient() {
  const client = net.connect({ port: 9090, host: 'www.opencord.chat' }, () => {
    console.log('Connected to server');
    // console.log("Message: ", chat.message);

    // Send data to the server
    client.write(JSON.stringify(chat.message));
  });

  
  let message_data = tools.readJSON(chat.message_path);
  let account_data = tools.readJSON(chat.account_path);
  console.log(account_data);
  // console.log("MessageData: ", message_data);

  let m = null; 
  chat.sock = client; 
  chat.profile_hash = account_data.name; 
  chat.username = account_data.UUID; 
  let matches = [];
  let changes = false;
  let parsed = null; 

  // Handle data from the server
  client.on('data', (data) => {
    console.log(`Received data from server: ${data}`);
    // console.log(`Received data from server: \n`);
    // const pattern = /\{([^}]+)\}/g;
    const pattern = /^\{.*\}$/;
    const text = data.toString('utf-8');
    matches = text.match(pattern);   
    let new_messages = {}; 
    // console.log("Matches: ", matches);
    // if(matches != null){
    //   console.log("Matches[0]: ", matches);
    // }else{
    //   console.log("No matches found");
    // }



    if(matches != null){
      try{
          parsed = JSON.parse(matches[0]);
          console.log("Parsed: ", parsed);
        if(parsed == null || parsed.length == 0){
          throw new Error("No valid data found"); 
        }
        
        // console.log("Parsed[0] ", parsed[0]);

        // m = text.split(matches[0]);
        // m = m[1]
        if(parsed.hasOwnProperty("size")){
          console.log("Size message");
        }else if(parsed.hasOwnProperty("0")){
          console.log("Message Bundle");
          const k_num = Object.keys(parsed).length; 
          changes = false
          for(let i = k_num - 1; i >= 0; i--){
            let i_str = String(i); 
            // console.log(parsed[i]);              
            // console.log("Parsed[i][id]: ", parsed[i]["id"]);
            // console.log("Object.keys(message_data) ", Object.keys(message_data));
            let keys = Object.keys(message_data);
            let item = parsed[i]["id"].toString();

            // if(!(item in keys)){
            if(!(message_data.hasOwnProperty(item))){
              changes = true; 
              console.log("X: ", keys); 
              console.log("Parsed i: ", item);
              let k = (Object.keys(new_messages).length); 
              new_messages[k] = parsed[i];
              message_data[item] = parsed[i];  
            }
            // createChatMessage(parsed[i]["content"], null, parsed[i]["m_from"], parsed[i]["m_time"]); 
          }

        }else if (parsed.hasOwnProperty("type")){
          if(parsed["type"] == 3){
            // console.log("Update the items");
            // console.log("Rooms: ", parsed["rooms"]);
            sendMessageToRenderer({"update-server": parsed});
          }

        }else{
          console.log("Something else. \n"); 
        }

      }catch(error){
        console.log("Error: ", error);
        console.log("JSON Error");
        // console.log(data.toString('utf-8'));
      }
  }else{
    console.log("Text only: ", text);
  }
  // Only write if changes are detected
  if(changes){
    console.log("Wrote: ", new_messages);

    // sendMessageToRenderer({"update": message_data}); 
    sendMessageToRenderer({"update": new_messages}); 


    tools.writeJSON(chat.message_path, message_data);
    // console.log("Send message to renderer"); 
    // checkProcessType();

    // send a message to renderer process 
    changes = false; 
  }

    
  });

  // Handle server disconnection
  client.on('end', () => {
    console.log('Disconnected from server');
  });
  return client;
}






// Start the TCP client

module.exports = {startClient, chat};