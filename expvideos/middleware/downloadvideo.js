module.exports = function(req, res, next) {
    // 1. Check all info in req
    if (!req.body.downloadLink) {
        res.status(400).json({ error: true, 
            message: `Request cannot be processed, missing required video identifier.`});
        return; 
    }
    else {
        const videoPath = req.body.downloadLink;
        try {
            res.download(videoPath);
        }
        catch (err) {
            res.status(410).json({ error: true, message: err.message });
        }
    };
};