const express = require('express')
const passport = require('passport')

function authenticated() {
    const app = express()

    app.use(passport.initialize());
    app.use(passport.session());

    // ruleid: express-route-authenticated
    app.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })

    // ruleid: express-route-authenticated
    app.post('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // todoruleid: express-route-authenticated
    app['post']('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // ruleid: express-route-authenticated
    app.delete('/', (req, res) => {
      res.send('DELETE request to the homepage')
    })
}

function unauthenticated() {
    const app = express()

    // ruleid: express-route-unauthenticated
    app.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })
}
