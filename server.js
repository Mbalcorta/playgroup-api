var firebase = require("firebase-admin");
var PythonShell = require('python-shell');

var serviceAccount = require("./serviceAccountKey.json");

firebase.initializeApp({
  credential: firebase.credential.cert(serviceAccount),
  databaseURL: "https://tag-app-8372b.firebaseio.com"
});

var db = firebase.database();

var myPythonScriptPath = 'eventsData.py';

// Use python shell

var pyshell = new PythonShell(myPythonScriptPath);
const allEventsArray = []

pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    const eventsPath = db.ref('libraryEvents')
    allEvents = JSON.parse(message)
    eventsPath.set(allEvents)
  });

db.ref().on("value", function(snapshot) {
  const events = snapshot.val()
  console.log(events['libraryEvents']['melrose_library'][1])
}, function (error) {
  console.log("Error: " + error.code);
});

// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err){
        throw err;
    };

    console.log('finished');
});

// var usersRef = ref.child("users");
// usersRef.set({
//   alanisawesome: {
//     date_of_birth: "June 23, 1912",
//     full_name: "Alan Turing"
//   },
//   gracehop: {
//     date_of_birth: "December 9, 1906",
//     full_name: "Grace Hopper"
//   }
// });