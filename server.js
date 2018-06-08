var firebase = require("firebase-admin");
var PythonShell = require('python-shell');

var serviceAccount = require("./serviceAccountKey.json");

firebase.initializeApp({
  credential: firebase.credential.cert(serviceAccount),
  databaseURL: "https://tag-app-8372b.firebaseio.com"
});

var db = firebase.database();

const myPythonScriptPath = 'eventsData.py';
const pyshell = new PythonShell(myPythonScriptPath);
const allEventsArray = []

//figure out way to trigger cron job at midnight for this to pull data from sites everyday

pyshell.on('message', function (message) {
    const eventsPath = db.ref('libraryEvents')
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