module.exports = function(req, res, next) {
    // 1. Check all info in req
    if (!req.user.id || !req.convertedVid || !req.body.video.id || !req.body.video.title ||
         !req.body.video.thumbnail || !req.body.video.length) {
        res.status(400).json({ error: true, 
            message: `Request body incomplete, missing required video data.`});
        return; 
    }
    else {
        const vId = req.body.video.id;
        const uId = req.user.id;
        const vTitle = req.body.video.title;
        const vThumbnail = req.body.video.thumbnail;
        const vLength = req.body.video.length;
        const videoPath = req.convertedVid;

        req.db
        .into("videos")
        .insert({videoId: vId, userId: uId, title: vTitle, thumbnail: vThumbnail, length: vLength})
        .then(() => {
            res.download(videoPath);
        })
        .catch((e) => {
            res.status(409).json({ error: true, message: e.message });
        });
    };
};