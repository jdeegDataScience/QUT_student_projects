module.exports = function(req, res, next) {
    // 1. Check job/info in req
    if (!req?.jobId || !req.jobs[req.jobId]?.metadata) {
        console.error('Error accessing jodId and metadata');
        req.sendToUser(
            req.userId, 'job-error',
            { error: 'Error accessing jodId and metadata' }
        );
        return; 
    }
    else {
        const vId = req.jobs[req.jobId].metadata.videoId;
        const uId = req.jobs[req.jobId].metadata.userId;
        const vTitle = req.jobs[req.jobId].metadata.title;
        const vThumbnail = req.jobs[req.jobId].metadata.thumbnail;
        const vLength = req.jobs[req.jobId].metadata.length;

        req.db
        .into("videos")
        .insert({videoId: vId, userId: uId, title: vTitle, thumbnail: vThumbnail, length: vLength})
        .catch((err) => {
            console.error('Error during db insert: ', req.jobs[req.jobId].metadata.title);
            console.error('Error: ', err.message);
            req.jobs[req.jobId].status = 'error';
            req.jobs[req.jobId].error = err.message;
            req.sendToUser(
                req.jobs[req.jobId].metadata.userId, 'job-error',
                { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, error: err.message }
            );
            // res.status(409).json({ error: true, message: err.message });
        });
        next();
    };
};