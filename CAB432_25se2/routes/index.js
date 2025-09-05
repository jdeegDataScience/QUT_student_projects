const express = require('express');
const router = express.Router();

const videosRouter = require("./videos");
const videoDetailsRouter = require("./videoDetails");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'The Video Converter Server' });
});

router.use('/videos', videosRouter);
router.use('/videoDetails', videoDetailsRouter);

module.exports = router;
