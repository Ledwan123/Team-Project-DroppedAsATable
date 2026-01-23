const express = require('express');
const path = require('path');
const bodyParser = require('body-parser')
const app = express();
const port = 8080;

//load static resources
app.use(express.static(path.join(__dirname, 'public')));
app.use('/assets', express.static(path.join(__dirname, 'public')));

//load dynamic resources
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.set('views', './views');

//get request for homepage
app.get('/', (req, res) => {
});

app.post('/login', (req, res) => {
  //access query parameters
  const user = req.body[userID];

  res.render('user', {
    title: 'Express Template Example',
    message: 'Hello user ${user}!',
    items: ['Item 1', 'Item 2', 'Item 3']
  });
})



app.listen(port, () => {
  console.log(`Express server running at http://localhost:${port}`);
});