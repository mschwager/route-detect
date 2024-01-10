import express, { Request, Response, Router } from 'express';
import passport from 'passport';


function authenticated() {
    const router1 = Router()
    const router2 = express.Router()
    const app = express()

    router1.use(passport.initialize());
    router1.use(passport.session());

    router2.use(passport.initialize());
    router2.use(passport.session());

    app.use(passport.initialize());
    app.use(passport.session());

    // ruleid: express-route-authenticated
    router1.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })

    // ruleid: express-route-authenticated
    router1.post('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // https://github.com/returntocorp/semgrep/issues/7290
    // todoruleid: express-route-authenticated
    router1['post']('/', (req, res) => {
      res.send('POST request to the homepage')
    })

    // ruleid: express-route-authenticated
    router2.delete('/', (req, res) => {
      res.send('DELETE request to the homepage')
    })

    // ruleid: express-route-authenticated
    app.get('/', (req, res) => {
      res.send('hello world')
    })
}

function unauthenticated() {
    const router1 = Router()
    const router2 = express.Router()
    const app = express()

    // ruleid: express-route-unauthenticated
    router1.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })

    // ruleid: express-route-unauthenticated
    router2.delete('/', (req, res) => {
      res.send('DELETE request to the homepage')
    })

    // ruleid: express-route-unauthenticated
    app.get('/', (req, res) => {
      res.send('hello world')
    })
}
