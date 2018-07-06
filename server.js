var firebase = require("firebase-admin");
var PythonShell = require('python-shell');
var path = require("path");

var serviceAccount = require("./serviceAccountKey.json");

firebase.initializeApp({
  credential: firebase.credential.cert(serviceAccount),
  databaseURL: "https://tag-app-8372b.firebaseio.com"
});

var db = firebase.database();

const addFirebaseContent = (fileName, dbRef) => {

    var options = {
        pythonPath: "/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"
      };

    const myPythonScriptPath = fileName;
    const pyshell = new PythonShell(myPythonScriptPath, options);
   
    const allEventsArray = []
    
    //figure out way to trigger cron job at midnight for this to pull data from sites everyday
    
    pyshell.on('message', function (message) {
        console.log(message)
        const eventsPath = db.ref(dbRef)
        allEvents = JSON.parse(message)
        eventsPath.set(allEvents)
      });
    
    pyshell.end(function (err) {
        if (err){
            throw err;
        };
        console.log('finished');
        process.exit()
    });
}

//need to figure out how to make one call after another
//can't do both calls at the same time
// addFirebaseContent('lotusBloomEvents.py', 'allendaleEvents')
addFirebaseContent('libraryEvents.py', 'libraryEvents')

