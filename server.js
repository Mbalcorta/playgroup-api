const express = require('express')
const PythonShell = require('python-shell');

const app = express();

app.get('/', callEventData);

function callEventData(req, res) {
  PythonShell.run('./eventsData.py', function (err, data) {
    if (err) res.send(err);
    res.send(data.toString())
  });
}

app.listen(3000, function () {
  console.log('server running on port 3000')
})