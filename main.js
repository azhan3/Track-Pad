const { app, BrowserWindow } = require('electron')

let win;


function createWindow () {
   win = new BrowserWindow({
      width: 800,
      height: 540,
      autoHideMenuBar: true,
      webPreferences: {
         nodeIntegration: true
      }
   })

   win.loadURL('http://localhost:5000');
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
   if (process.platform !== 'darwin') {
      app.quit()
   }
})

app.on('activate', () => {
   if (win === null) {
      createWindow()
   }
})