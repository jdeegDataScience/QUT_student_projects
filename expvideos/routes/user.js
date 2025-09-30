const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET;
const bcrypt = require('bcrypt');
const express = require('express');
const router = express.Router();

const userExists = require("../middleware/postuserexists");
const generateTokens = require("../middleware/generatetokens");
const hasRefreshToken = require("../middleware/postuserhasrefreshtoken");
const authorisation = require("../middleware/authorisation");
const invalidatetoken = require("../middleware/invalidatetoken");

/* POST user login; auth token */
router.post('/login', userExists, function(req, res, next) {
    // If user does not exist, throw error
    if (!req.match) {
        throw new Error(`Incorrect email or password`);
    }
    else {
        const password = req.body.password;
        // If user does exist, verify if passwords match
        bcrypt.compare(password, req.user.hash)
        .then((match) => {
            if (!match) {
                throw new Error("Incorrect email or password");
            }
            else {
                next();
            }
        })
        .catch((e) => {
            res.status(401).json({ error: true, message: e.message });
            return;
        });
    };}, 
    invalidatetoken, generateTokens
);

/* POST register user; add to db */
router.post('/register', userExists, function(req, res) { 
    // If user does exist, throw error
    if (req.match) {
        throw new Error(`User already exists`);
    }
    // If user does not exist, insert into table
    else {
        const email = req.body.email;
        const password = req.body.password;
        // Insert user into DB
        const saltRounds = 10;
        const hash = bcrypt.hashSync(password, saltRounds);
        req.db.from("users").insert({ email, hash })
        .then(() => {
            res.status(201).json({message: "User created"});
        })
        .catch((e) => {
            res.status(409).json({ error: true, message: e.message });
        });
    };
    return;
});

/* POST refresh token */
router.post('/refresh', hasRefreshToken, authorisation, invalidatetoken, generateTokens);

/* POST refresh token */
router.post('/logout', hasRefreshToken, authorisation, invalidatetoken, function(req, res) {
    res.status(200).json({error: false, message: 'Token successfully invalidated'});
});

/* GET users listing. */
router.get('/', function(req, res, next) {
    req.db.from("users").select('userId', 'email')
    .then((rows) => { 
        res.status(200).json({ Error: false, Message: "Success", Users: rows }); 
    });
});

module.exports = router;
