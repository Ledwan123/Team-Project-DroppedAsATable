const { createServer } = require('node:http');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = 3000;

const server = createServer((req, res) => {
    var data = fs.readFileSync("index.html");
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end(data);
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
