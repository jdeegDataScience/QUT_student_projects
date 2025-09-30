const express = require('express');
const router = express.Router();

const getvideos = require("../middleware/getvideos");
// const convertvideo = require("../middleware/convertyoutubevideo");
// const getvideoinfo = require("../middleware/getvideoinfo");
const insertmetadata = require("../middleware/insertmetadata");
const downloadvideo = require("../middleware/downloadvideo");
const hasbearertoken = require("../middleware/hasbearertoken");
const authorisation = require("../middleware/authorisation");
const getuserid = require("../middleware/getuserid");
const cobalt = require("../middleware/cobalt");

router.post('/convert', hasbearertoken, authorisation, getuserid, /* getvideoinfo, convertvideo, */ insertmetadata);

router.get('/download', hasbearertoken, authorisation, downloadvideo);

router.get('/cobalt', cobalt);

router.use('/', hasbearertoken, authorisation, getuserid, getvideos);

router.get('/', function(req, res, next) {
    const pageNum = req.query?.page ? parseInt(req.query.page) : 1;
    const perPage = 5; // number of videos in each page 
    const totalVideos = req.videos?.length;
    const last = Math.ceil(totalVideos/perPage);
    const pageStart = (pageNum - 1) * perPage; // start index of requested rows set 
    const pageEnd = totalVideos - pageStart < 10 ? totalVideos : pageStart+10;

    const currPageVideos = req.videos.slice(pageStart, pageEnd);
    Promise.resolve(currPageVideos.map((video) => ({
        id: video.videoId,
        title: video.title,
        imgUrl: video.thumbnail,
        length: Number(video.length),
        ts: video.ts,
        
    })))
    .then((videos) => {
        res.json({ data: videos, pagination: {total: totalVideos, lastPage: last, perPage: perPage, currentPage: pageNum, from: pageStart, to: pageEnd } });
    });
});

/* GET videos page. */
// router.get('/', function(req, res, next) {
//   res.render('index', { title: 'The Videos Search Page' });
// });

module.exports = router;