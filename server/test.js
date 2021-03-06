const express = require('express')
const app = express();
const path = require("path");
const port = process.env.PORT || 3001;
const fs = require("fs");
var http = require('http');

// TO-USE REFERENCE: https://github.com/myogeshchavan97/express-static-serve/tree/master/react-app

// or use https://github.com/reactjs/express-react-views for server-side rendering only...


// app.db // to-do
// app.set('views', __dirname + '/views');
app.set('root', __dirname)
// app.use(express.logger('dev'));
// app.use(express.static(__dirname + '/public'));


// app.use(express.static(path.join(__dirname, 'client/build')));
// app.use(express.static(path.join(__dirname, ".." ,'build')));


app.use(express.static(path.resolve(__dirname, '../client')));


// app.use(express.static("public"));

app.get("/api/list", (req, res) => {
    var list = ["Hello", "from", "server"];
    res.json(list);
    console.log(list);
});


app.get("/api", (req, res) => {
	res.json({ message: "Hello from server!" });
});




app.get('*', (req, res) => {
	res.sendFile(path.resolve(__dirname, '../client', 'index.html'));
});

// app.use((req, res, next) => {
//     res.sendFile(path.join(__dirname, "..", "build", "index.html"));
//   });

// app.use(app.router); // do not know how to use with components....



var server = http.createServer(app);

// require('./routes/main');

// // dynamically load routes
// fs.readdirSync('./routes/').forEach(function (file) {
//     var route = './routes/' + file;
//     require(route)(app);
// });

server.listen(port);

// app.use(express.static(path.join(__dirname, "client", "build")));

// app.listen(PORT, () => {
//     console.log(`Server listening on port ${PORT}`);
// })

// app.get('/*', (req, res) => {
//     res.sendFile(path.join(__dirname, '../', 'client', 'build', 'index.html'));
// });