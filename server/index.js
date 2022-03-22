// const express = require('express')


// import router from './routes/main.js';
// import express from 'express';
// import path from 'path';
// import bodyParser from 'body-parser';
// import cors from 'cors';
// import fs from 'fs';
// import * as child from 'child_process';

const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const fs = require('fs')
const cors = require('cors')


const app = express();
// const path = require("path");
const port = process.env.PORT || 8000;
// const fs = require("fs");
// const bodyParser = require("body-parser");
// var http = require('http');

app.use(bodyParser.json({ limit: '10mb', extended: true }));
app.use(bodyParser.urlencoded({ limit: '10mb', extended: true }))
app.use(cors());


// https://stackoverflow.com/questions/23450534/how-to-call-a-python-function-from-node-js

// let runPy = new Promise(function(success, nosuccess) {

//     const { spawn } = require('child_process');
//     const pyprog = spawn('python', ['./assets/py_services/get_neighbourhoods.py', ]);

//     pyprog.stdout.on('data', function(data) {

//         success(data);
//     });

//     pyprog.stderr.on('data', (data) => {

//         nosuccess(data);
//     });
// });



// app.use(express.static(path.resolve(__dirname, '../client/build')));

app.get('/api/getNeighbourhoods', (req, res) => {
    //to-do: get real neighbourhood list from csv
    // const neighbourhoodOptions = require('./assets/data_files/clean-nbr-coords.json');
    // var list = ["NB1 from Server", "NB2 from Server", "NB3 from Server"];
    // res.json(list);
    // console.log(list);
    fs.readFile('./assets/data_files/clean-nbr-coords.json', function (error, content) {
        var data = JSON.parse(content);
        var neighbourhoodOptions = data.neighbourhood
        res.json(neighbourhoodOptions);
        console.log(neighbourhoodOptions);
    });

});

app.post('/api/search', (req, res) => {
    var options = {
        root: path.join(__dirname)
    };


    //to-do: process with find_hotel
    console.log(req.body)

    // var content = JSON.parse(req.body);
    var content = req.body;
    var chosen_nbr = content.neighbourhood
    var chosen_amns = content.amenityPriorityByType

    const { spawn } = require('child_process');
    const pyprocess = spawn('python', ['./assets/py_services/get_neighbourhoods.py'], content);

    // // https://medium.com/swlh/run-python-script-from-node-js-and-send-data-to-browser-15677fcf199f
    // pyprocess.stdout.on('data', function (data) {
    //     console.log('Pipe data from python script ...');
    //     dataToSend = data.toString();
    // });
    // in close event we are sure that stream from child process is closed
    // pyprocess.on('close', (code) => {
    //     console.log(`child process close all stdio with code ${code}`);
    //     // send data to browser
    //     // res.send(dataToSend)
    //     res.sendFile('assets/py_output/result.html', options);
    // });
});
app.get('/api/map-result', (req, res) => {
    res.sendFile('assets/py_output/result.html', options);
});



app.get('/api/list', (req, res) => {
    var list = ["Hello", "from", "server"];
    res.json(list);
    console.log(list);
});


app.get("/api", (req, res) => {
	res.json({ message: "Hello from server!" });
});

// app.get('*', (req, res) => {
// 	res.sendFile(path.resolve(__dirname, '../client/build', 'index.html'));
// });

// app.use((req, res, next) => {
//     res.sendFile(path.join(__dirname, "..", "build", "index.html"));
//   });

// app.use(app.router); // do not know how to use with components....



// var server = http.createServer(app);

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});



// require('./routes/main');

// // dynamically load routes
// fs.readdirSync('./routes/').forEach(function (file) {
//     var route = './routes/' + file;
//     require(route)(app);
// });

// server.listen(port);

// app.use(express.static(path.join(__dirname, "client", "build")));


// app.get('/*', (req, res) => {
//     res.sendFile(path.join(__dirname, '../', 'client', 'build', 'index.html'));
// });