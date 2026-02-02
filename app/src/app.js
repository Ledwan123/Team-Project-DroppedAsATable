// Configures Express
const compression = require('compression');
const express = require("express");
const path = require('path');

const app = express();
const routes = require('./routes')

// Allows server to automatically handle JSON a
// app.use(express.json());
// urlencoded?

// Routes
app.use("/", routes);

// Allows us to serve static files via Express
app.use('/static', express.static(path.join('/workspaces/Team-Project-DroppedAsATable/app/', 'public')));

// Compress all HTTP responses
app.use(compression());


module.exports = app;