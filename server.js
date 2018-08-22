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
    return new Promise(function(resolve, reject) {
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
    
    return pyshell.end(function (err) {
            if (err){
              return reject(err);
            };
            return resolve('finished');
            process.exit()
        })  
    });
}

addFirebaseContent('libraryEvents.py', 'libraryEvents')
.then(response => console.log(response))
.then(addFirebaseContent('lotusBloomEvents.py', 'allendaleEvents'))
.catch(error => console.log(error))

