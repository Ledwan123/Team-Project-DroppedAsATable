const compression = require('compression');
const express = require("express");
const fs = require("fs");
const path = require('path');

const app = express();

// Allows us to serve static files via Express
app.use('/static', express.static(path.join('/workspaces/Team-Project-DroppedAsATable/app/', 'public')));

// Compress all HTTP responses
app.use(compression());

// Home page
app.get("/", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

// Signup.html request functions
app.get("/signup.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/signup.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

// Signup.html request functions
app.get("/login.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

// Tells the server to listen for requests on specificed port, if specified port isn't set them defaults to 3000.
app.listen(process.env.PORT || 3000, () => console.log("App available on http://localhost:3000"));
