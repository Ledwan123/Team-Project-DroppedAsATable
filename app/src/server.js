// Starts the server
const app = require('./app');

// Tells the server to listen for requests on specificed port, if specified port isn't set them defaults to 3000.
app.listen(process.env.PORT || 3000, () => console.log("App available on http://localhost:3000"));
