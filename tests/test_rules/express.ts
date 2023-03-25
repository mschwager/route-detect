import express, { Request, Response, Router } from 'express';
import passport from 'passport';


function authenticated() {
    const router1 = Router()
    const router2 = express.Router()

    router1.use(passport.initialize());
    router1.use(passport.session());

    router2.use(passport.initialize());
    router2.use(passport.session());

    // ruleid: express-route-authenticated
    router1.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })

    // ruleid: express-route-authenticated
    router1.post('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // todoruleid: express-route-authenticated
    router1['post']('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // ruleid: express-route-authenticated
    router2.delete('/', (req, res) => {
      res.send('DELETE request to the homepage')
    })
}

function unauthenticated() {
    const router1 = Router()
    const router2 = express.Router()

    // ruleid: express-route-unauthenticated
    router1.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })

    // ruleid: express-route-unauthenticated
    router2.delete('/', (req, res) => {
      res.send('DELETE request to the homepage')
    })
}
