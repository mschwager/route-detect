const express = require('express')
const app = express()

// ruleid: express-route
app.get('/', (req, res) => {
  res.send('GET request to the homepage')
})

// ruleid: express-route
app.post('/', (req, res) => {
  res.send('POST request to the homepage')
})

// todoruleid: express-route
app['post']('/', (req, res) => {
  res.send('POST request to the homepage')
})

// ruleid: express-route
app.delete('/', (req, res) => {
  res.send('DELETE request to the homepage')
})
