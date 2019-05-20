var electron = require('electron');
var _app = electron.app;
var BrowserWindow = electron.BrowserWindow;

var mainWindow = null;

// Quit when all windows are closed.
// app.on('window-all-closed', function () {
//     app.quit();
// });

_app.on('ready', function(){

    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 720
    })

    // and load the index.html of the app.
	//    mainWindow.loadURL('file://' + __dirname + '/app/index.html');
     mainWindow.loadURL('http://127.0.0.1:8000/pipelines');

    // Open the devtools.
//    mainWindow.openDevTools();

    // Emitted when the window is closed.
    mainWindow.on('closed', function () {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
        _app.quit();
  });

})

