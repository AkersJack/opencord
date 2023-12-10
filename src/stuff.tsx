import * as fs from 'fs';
import * as path from 'path';
import * as folderEncrypt from 'folder-encrypt';
import * as crypto from 'crypto-js';
import * as uuid from 'uuid';



function fileExists(filePath: string): boolean {
  try {
    // Check if the file exists
    fs.accessSync(filePath, fs.constants.F_OK);
    return true;
  } catch (err) {
    return false;
  }
}



// Done asynchronously
function write(fullpath: string, data:string){
    // const path = '../oc/other/';
    // const fullpath = path + file;
    console.log("writing: " + fullpath); 
    if (!(fileExists(fullpath))){
        fs.writeFile(fullpath, data, 'utf-8', (err) =>{
            if(err){
                console.log("Error creating file: ", err);
            }else{
                console.log("File created successfully"); 
            }
        });
        console.log('File has been written successfully.');
        return 0; 
    }
        fs.writeFile(fullpath, data, 'utf-8', (err) => {
            if (err) {
            console.error('Error writing to file:', err);
            return;
            }
            console.log('File has been written successfully.');
        });
        return 0;  
}

// Done asynchronously
function read(fullpath: string){
    // const path = '../oc/other/';
    // const fullpath = path + file; 
    if (!(fileExists(fullpath))){
            console.log("Error: File doesn't exist.");
        return "";
    }
    fs.readFile(fullpath, 'utf-8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return ""; 
    }
    console.log('File content:', data);
    return data; 


    });
}


function readJSON(fullpath: string){
    let data = {}; 
    if (!(fileExists(fullpath))){
            console.log("Error: File doesn't exist.");
        return {};
    }
    try{
        data = JSON.parse(fs.readFileSync(fullpath, 'utf-8')); 
    }catch(error){
        console.log("Error: Unable to parse JSON data. "); 
        return {}; 
    }
    return data; 
}
// const formattedJsonStr = JSON.stringify(jsonObject, null, 2);
// Asynchronous writeFileSync for synchronous (might cause issues)
function writeJSON(fullpath: string, data: Object){
        let data_str = JSON.stringify(data, null, 2); 
        if (!(fileExists(fullpath))){
            fs.writeFile(fullpath, data_str, 'utf-8', (err) =>{
                if(err){
                    console.log("Error: ", err);
                    return 1; 
                }else{
                    console.log("JSON file created successfully"); 
                }
            });
            console.log('JSON file has been written successfully.');
            return 0; 
        }
        fs.writeFile(fullpath, data_str, 'utf-8', (err) => {
            if (err) {
            console.error('Error:', err);
            return 1; 
            }
            console.log('JSON file has been written successfully.');
        });
        return 0;  
}

const dirpath = path.resolve(__dirname, '../..');
const filepath = path.join(dirpath, '/oc/');
console.log("Filepath: " + filepath); 

async function deleteFolderRecursive(folderPath: string) {
  try {
    const files = await fs.promises.readdir(folderPath);
    for (const file of files) {
      const filePath = path.join(folderPath, file);
      const stats = await fs.promises.stat(filePath);
      if (stats.isFile()) {
        await fs.promises.unlink(filePath);
      } else if (stats.isDirectory()) {
        await deleteFolderRecursive(filePath);
      }
    }
    await fs.promises.rmdir(folderPath);
  } catch (error) {
    console.error(`Error deleting folder: ${error}`);
  }
}


function encryptFile(filePath: string, password: string,  isRecursive: boolean): void{



    if(isRecursive){
        const files = fs.readdirSync(filePath, 'utf8');
        console.log("Files: ", files);
        files.forEach((item) =>{
            if(!item.endsWith('.encrypted')){
            const newFilePath_enc = path.join(filePath, item + ".encrypted");
            const newFilePath = path.join(filePath, item);
            const filecontent = fs.readFileSync(newFilePath, 'utf8');
            const encryptedContent = crypto.AES.encrypt(filecontent, password).toString();
            fs.writeFileSync(newFilePath_enc, encryptedContent, 'utf8'); 
            console.log("File encrypted: ", newFilePath_enc);
            fs.unlinkSync(newFilePath);
            }
            });

    }else{

    // const fileContent = fs.readFileSync(filePath, 'utf8');
    // const encryptedContent = crypto.AES.encrypt(fileContent, password).toString(); 
    // const newFilePath = filePath + '.enc'; 
    console.log("encrypt single file.");
    }

    // fs.writeFileSync(newFilePath, encryptedContent, 'utf8')

    // console.log("File encrypted: ", filePath);


   
}

function decryptFile(filePath: string, password: string, isRecursive: boolean): int{
    try{
        if(isRecursive){
            const files = fs.readdirSync(filePath);
            console.log("Files: ", files);
            files.forEach((item) =>{
                const newFilePath_enc = path.join(filePath, item);
                const newFilePath = path.join(filePath, item.split('.encrypted')[0]);
                const encryptedFile = fs.readFileSync(newFilePath_enc, 'utf8');
                const decryptContent = crypto.AES.decrypt(encryptedFile, password).toString(crypto.enc.Utf8);
                fs.writeFileSync(newFilePath, decryptContent, 'utf8'); 
                console.log("decrypted content: ", decryptContent);
                console.log("File Decrypted: ", newFilePath);
                // fs.unlinkSync(newFilePath_enc);
                });
        }

    }catch(error){
        console.log("Error decrypting file: ", error);
        return 1; 

    }
    return 0; 

}



function encryptDirectory(directoryPath: string, password: string): void {
  encryptFile(directoryPath, password, true);
}

function decryptDirectory(directoryPath: string, password: string): void {
    decryptFile(directoryPath, password, true);
}


/* Old Encryption (doesn't work very well)

function encryptFolder(username: string, password: string){
    console.log("Encrypting folder...");
    const folderPath = path.join(filepath, '/', username);
    try{
        if(!fs.existsSync(folderPath)){
            throw new Error("Folder does not exist."); 
        }
        folderEncrypt.encrypt({
            password: password,
            input: folderPath, 
        }).then(() =>{
            console.log("Folder encrypted successfully!");
            try{
                deleteFolderRecursive(folderPath); // Delete unencrypted folder
            }catch(error){
                console.log("Error deleting unencrypted folder: ", error);
            }
        }).catch((err) =>{
            console.log("Error encrypting folder: ", err);
        });

    }catch (encryptError) {
        console.log("Error encrypting: ", encryptError);
    }
    return 0; 
}

function decryptFolder(username: string, password: string){
    const folderPath = path.join(filepath, '/', (username + ".encrypted"));
    // const newPath = path.join(filepath, '/', (username + "_old.encrypted"));
    try{
        if(!fs.existsSync(folderPath)){
            throw new Error("Encrypted item does not exist."); 
        }
    folderEncrypt.decrypt({
        password: password,
        input: folderPath, 
    }).then(() =>{
        console.log("Folder decrypted successfully!");
        // fs.renameSync(folderPath,  newPath);
        // try{
        //     deleteFolderRecursive(folderPath); // Delete unencrypted folder
        // }catch(error){
        //     console.log("Error deleting unencrypted folder: ", error);
        // }
    }).catch((err) =>{
        console.log("Error decrypting folder: ", err);
    });
    }catch(decryptError){
        console.log("Error decrypting: ", decryptError);
    }
    
}
*/

function createAccount(username: string, password: string){
    const folderPath = path.join(filepath, '/', username);
    const accountDetails = path.join(folderPath, "account.json")

    const data: any = {
        UUID: uuid.v4(),
        name: username, 
    };

    const jsonString = JSON.stringify(data, null, 2);


    try{
        if(!fs.existsSync(folderPath)){
            fs.mkdirSync(folderPath);
            console.log('Folder created successfully!');
        }else{
            console.log("Falder already exists on desktop."); 
            // Throw error here for user already exists
        }
        // const subfolder = path.join(folderPath, )
        const messages_file = path.join(folderPath, 'messages.json');
        const data = '';
        fs.writeFileSync(messages_file, data);
        fs.writeFileSync(accountDetails, jsonString);
        console.log("Account Details written successfully!");

    }catch(error){
        console.error('Error creating folders: ', error); 
    }

    // console.log("Folder path encrypt: ", folderPath);
    // encryptFolder(username, password);
    encryptDirectory(folderPath, password);

}



module.exports = {read, write, fileExists, readJSON, writeJSON, createAccount, encryptFile, encryptDirectory, decryptFile, decryptDirectory};