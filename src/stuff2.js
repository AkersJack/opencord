"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require("fs");
function fileExists(filePath) {
    try {
        // Check if the file exists
        fs.accessSync(filePath, fs.constants.F_OK);
        return true;
    }
    catch (err) {
        return false;
    }
}
// Done asynchronously
function write(fullpath, data) {
    // const path = '../oc/other/';
    // const fullpath = path + file;
    console.log("writing: " + fullpath);
    if (!(fileExists(fullpath))) {
        fs.writeFile(fullpath, data, 'utf-8', function (err) {
            if (err) {
                console.log("Error creating file: ", err);
            }
            else {
                console.log("File created successfully");
            }
        });
        console.log('File has been written successfully.');
        return 0;
    }
    fs.writeFile(fullpath, data, 'utf-8', function (err) {
        if (err) {
            console.error('Error writing to file:', err);
            return;
        }
        console.log('File has been written successfully.');
    });
    return 0;
}
// Done asynchronously
function read(fullpath) {
    // const path = '../oc/other/';
    // const fullpath = path + file; 
    if (!(fileExists(fullpath))) {
        console.log("Error: File doesn't exist.");
        return "";
    }
    fs.readFile(fullpath, 'utf-8', function (err, data) {
        if (err) {
            console.error('Error reading file:', err);
            return "";
        }
        console.log('File content:', data);
        return data;
    });
}
function readJSON(fullpath) {
    var data = {};
    if (!(fileExists(fullpath))) {
        console.log("Error: File doesn't exist.");
        return {};
    }
    try {
        data = JSON.parse(fs.readFileSync(fullpath, 'utf-8'));
    }
    catch (error) {
        console.log("Error: Unable to parse JSON data. ");
        return {};
    }
    return data;
}
// const formattedJsonStr = JSON.stringify(jsonObject, null, 2);
// Asynchronous writeFileSync for synchronous (might cause issues)
function writeJSON(fullpath, data) {
    var data_str = JSON.stringify(data, null, 2);
    if (!(fileExists(fullpath))) {
        fs.writeFile(fullpath, data_str, 'utf-8', function (err) {
            if (err) {
                console.log("Error: ", err);
                return 1;
            }
            else {
                console.log("JSON file created successfully");
            }
        });
        console.log('JSON file has been written successfully.');
        return 0;
    }
    fs.writeFile(fullpath, data_str, 'utf-8', function (err) {
        if (err) {
            console.error('Error:', err);
            return 1;
        }
        console.log('JSON file has been written successfully.');
    });
    return 0;
}
module.exports = { read: read, write: write, fileExists: fileExists, readJSON: readJSON, writeJSON: writeJSON };
