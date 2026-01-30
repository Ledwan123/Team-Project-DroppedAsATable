const express = require("express");
const fs = require("fs");

const app = express();

app.get("/home.html");

app.get("/", (req, res) => {

    fs.readFile("/workspaces/Team-Project-DroppedAsATable/app/views/home.html", "utf8", (err, html) => {
        if (err) {
            res.status(500).send("INTERNAL SERVER ERROR");
        }
        
        res.send(html);
    })

});

app.listen(process.env.PORT || 3000, () => console.log("App available on http://localhost:3000"));
