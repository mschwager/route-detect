const express = require('express')
const passport = require('passport')
const { auth, requiresAuth } = require('express-openid-connect')
const { expressjwt: jwt } = require('express-jwt')

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

function oidc() {
    const app = express()

    app.use(
        auth({
            issuerBaseURL: process.env.AUTH0_ISSUER_BASE_URL,
            baseURL: process.env.BASE_URL,
            clientID: process.env.AUTH0_CLIENT_ID,
            secret: process.env.SESSION_SECRET,
            authRequired: true,
            auth0Logout: true,
        }),
    );

    // ruleid: express-route-authenticated
    app.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })
}

function jwt() {
    const app = express()

    app.use(
        jwt({
            secret: "secret",
            algorithms: ["HS256"],
        }),
    );

    // ruleid: express-route-authenticated
    app.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })
}

function inline() {
    const app = express()

    // todoruleid: express-route-authenticated, express-route-unauthenticated
    app.get(
        '/protected',
        expressjwt({ secret: "secret", algorithms: ["HS256"] }),
        (req, res) => {
            res.send('GET request to the homepage')
        }
    )

    // todoruleid: express-route-authenticated, express-route-unauthenticated
    app.get(
        '/protected',
        requiresAuth(),
        (req, res) => {
            res.send('GET request to the homepage')
        }
    )
}

function unauthenticated() {
    const app = express()

    // ruleid: express-route-unauthenticated
    app.get('/', (req, res) => {
      res.send('GET request to the homepage')
    })
}
