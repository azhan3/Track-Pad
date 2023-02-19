/*
+-------------------------------------------------------------------------+
| This file contains the code to set up the Electron.js desktop window    |
| It connects to a Python backend Flask framework through localhost:16969 |
+-------------------------------------------------------------------------+
*/
const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const express = require('express');
const path = require('path')
const appExpress = express();
const http = require('http');

// Reload endpoint to reload the page

appExpress.get('/reload', (req, res) => {
   console.log('reloading page');

   // Reload all windows

   BrowserWindow.getAllWindows().forEach((win) => {
      win.reload();
   });
   res.send('page reloaded');
});


// Start the server and listen on port 46832

const server = http.createServer(appExpress);
server.listen(46832, 'localhost', () => {
   console.log('Server listening on port 46832');
});

// Browser window object

let win; 

// Python process object

let pythonProcess; 


// Create a new browser window

function createWindow() {
   win = new BrowserWindow({
      width: 800,
      height: 540,
      icon: __dirname + '/static/Assets/icon.ico',
      autoHideMenuBar: true,
      webPreferences: {
         
         // Enable Node.js integration in the browser window
         
         nodeIntegration: true 
      }
   });

   // Load the HTML file in the browser window

   win.loadURL('http://localhost:16969');

   // When the window is closed, set win to null and kill the Python process

   win.on('closed', () => {
      win = null;
      pythonProcess.kill();
   });
}


// Start the Python process

function startPythonProcess() {
   pythonProcess = spawn('python', ['main.py']);

   // Log standard output data from the Python process

   pythonProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
   });

   // Log standard error data from the Python process

   pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
   });

   // Log the exit code when the Python process is closed

   pythonProcess.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
   });
}


// Create the browser window and start the Python process when Electron is ready

app.whenReady().then(() => {
   createWindow();
   startPythonProcess();
});


// Quit the app when all windows are closed (except on macOS)

app.on('window-all-closed', () => {
   if (process.platform !== 'darwin') {
      app.quit();
   }
});


// Recreate the window if it's null when the app is activated (macOS only)

app.on('activate', () => {
   if (win === null) {
      createWindow();
   }
});


// Kill the Python process when the app is about to quit

app.on('before-quit', () => {
   console.log("Ended");
   pythonProcess.kill();
});


// Reload the window when the "reload-window" event is received from the renderer process

ipcMain.on('reload-window', () => {
   win.reload();
});
