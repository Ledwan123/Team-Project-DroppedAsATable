// Defining routes
const express = require('express');
const router = express.Router();
const fs = require("fs");

// Home page
router.get("/", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

// Signup.html request functions
router.get("/signup.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/signup.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

// Signup.html request functions
router.get("/login.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

router.post("/login.html", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/login.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

    

});

module.exports = router;