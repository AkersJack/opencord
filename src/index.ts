import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import * as url from 'url';

import * as net from 'net';
import { startClient, chat } from './client';
import * as stuff from './stuff';
import {createAccount, encryptFolder, decryptFolder} from './stuff.tsx';



// This allows TypeScript to pick up the magic constants that's auto-generated by Forge's Webpack
// plugin that tells the Electron app where to look for the Webpack-bundled app code (depending on
// whether you're running in development or production).
declare const MAIN_WINDOW_WEBPACK_ENTRY: string;
declare const MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY: string;

const dirpath = path.resolve(__dirname, "../../"); 

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

let mainWindow; 
let loginWindow;

let username; 
let password; 

const createWindow = (): void => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    height: 600,
    width: 800,
    webPreferences: {
      preload: MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY,
      nodeIntegration: true,
      contextIsolation: false,
    },
  });


  // and load the index.html of the app.
  mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);

  // Open the DevTools.
  mainWindow.webContents.openDevTools();

};

const createLoginWindow = (): void => {
  // Create the browser window.
  loginWindow = new BrowserWindow({
    height: 600,
    width: 800,
    webPreferences: { 
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  // loginWindow.loadFile(path.join(__dirname, '/login/index.html'))

  loginWindow.loadURL('file://C:/Users/jacka/Desktop/UMBC/cmsc447/opencord/opencord/src/main/index.html');


  // Open the DevTools.
  loginWindow.webContents.openDevTools();

};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', () =>{
  createWindow();

  // createLoginWindow();
  // loginWindow.hide();

});

app.on('ready', ()=>{
// Listen for IPC messages from the renderer process
  startClient();
  ipcMain.on('send-to-client', (event, message) => {
    // Forward the message to the TCP client
    // For simplicity, assuming there's only one client
    // You may need to modify this for multiple clients
    console.log("Message: ", message);
    chat.sock.write(chat.sendmsg(message));
  });
});


ipcMain.on('to-register', ()=>{
  // secondWindow.loadURL('file://C:/Users/jacka/Desktop/UMBC/cmsc447/opencord/opencord/src/login/index.html');
  console.log("Swapping windows");
  mainWindow.loadFile(path.join(dirpath, '/src/register/register.html'));
});

ipcMain.on('to-login', ()=>{
  console.log("to login");
  console.log("Swapping windows");
  // mainWindow.loadFile(path.join(dirpath, "/src/index.html"));
  mainWindow.loadURL(MAIN_WINDOW_WEBPACK_ENTRY);

});

ipcMain.on('register', (event, formData)=>{
  console.log("register");
  const data = JSON.parse(formData);
  const username = data.username;
  const password = data.password;
  console.log("Register Username: ", username);
  console.log("Register Password: ", password);
  stuff.createAccount(username, password); 

});

ipcMain.on('login', (event, formData)=>{
  console.log("login"); 
  const data = JSON.parse(formData);
  username = data.username;
  password = data.password;

  // console.log("Username: ", username);
  // console.log("Password: ", password);
  // console.log("Username: ", event.get('username'));

  // console.log("Username: ", event.get('password'));
  stuff.decryptFolder(username, password);


});




// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.

app.on('before-quit', ()=>{
  stuff.encryptFolder(username, password);
  console.log("Before quit: ");

});

app.on('window-all-closed', () => {
  console.log("During quit: ");
  if (process.platform !== 'darwin') {
    app.quit(
      stuff.encryptFolder(username, password);
    );
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});






// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.



