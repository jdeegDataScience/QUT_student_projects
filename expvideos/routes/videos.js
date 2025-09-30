const express = require('express');
const router = express.Router();

const getvideos = require("../middleware/getvideos");
const convertvideo = require("../middleware/convertyoutubevideo");
const getconvertedvideodata = require("../middleware/getconvertedvideo");
const hasbearertoken = require("../middleware/hasbearertoken");
const authorisation = require("../middleware/authorisation");
const getuserid = require("../middleware/getuserid");

router.use('/', hasbearertoken, authorisation, getuserid, getvideos);

router.get('/', function(req, res, next) {
    const pageNum = req.query?.page ? parseInt(req.query.page) : 1;
    const perPage = 10; // number of videos in each page 
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

router.use('/convert', hasbearertoken, authorisation, getuserid, convertvideo);

router.get('/convert', getconvertedvideodata);

/* GET videos page. */
// router.get('/', function(req, res, next) {
//   res.render('index', { title: 'The Videos Search Page' });
// });

/* router.use('/data/:imdbID', getvideosdata);

router.get('/data/:imdbID', function(req, res, next) {
    const genresArr = req.basicData.genres.split(",");
    res.status(200).json({
        title: req.basicData.title, 
        year: req.basicData.year,
        runtime: req.basicData.runtime,
        genres: genresArr,
        country: req.basicData.country,
        principals: req.principalsData,
        ratings: req.ratingsData,
        boxoffice: req.basicData.boxoffice,
        poster: req.basicData.poster,
        plot: req.basicData.plot
    });
}); */

module.exports = router;