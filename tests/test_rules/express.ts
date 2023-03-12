import express, { Request, Response, Router } from 'express';

const router1 = Router()
const router2 = express.Router()

// ruleid: express-route
router1.get('/', (req, res) => {
  res.send('GET request to the homepage')
})

// ruleid: express-route
router1.post('/', (req, res) => {
  res.send('POST request to the homepage')
})

// todoruleid: express-route
router1['post']('/', (req, res) => {
  res.send('POST request to the homepage')
})

// ruleid: express-route
router2.delete('/', (req, res) => {
  res.send('DELETE request to the homepage')
})
