// const express = require('express')


// import router from './routes/main.js';
import express from 'express';
import path from 'path';
import bodyParser from 'body-parser';
import cors from 'cors';
import fs from 'fs';

const app = express();
// const path = require("path");
const port = process.env.PORT || 8000;
// const fs = require("fs");
// const bodyParser = require("body-parser");
// var http = require('http');

app.use(bodyParser.json({ limit: '10mb', extended: true }));
app.use(bodyParser.urlencoded({ limit: '10mb', extended: true }))
app.use(cors());




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
    //to-do: process with find_hotel
    console.log(req.body)
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