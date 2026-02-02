const express = require("express");
const fs = require("fs");
const path = require('path');

const app = express();
app.use('/static', express.static(path.join('/workspaces/Team-Project-DroppedAsATable/app/', 'public')));

app.get("/home.html");

app.get("/", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

app.get("/signup.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/signup.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

app.get("/login.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});


app.listen(process.env.PORT || 3000, () => console.log("App available on http://localhost:3000"));
