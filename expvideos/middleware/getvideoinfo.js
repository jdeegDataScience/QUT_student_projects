// const path = require('path');
// const os = require('os');
// const { ytPromise } = require('./youtubestream');



// module.exports = async function(req, res, next) {
//     const yt = await ytPromise;
//     const youtubeUrl = req.body.video.url;

//     const ts = Date.now().toString();
//     const uId = req.user.id;
//     const jobId = uId + Date.now().toString();
//     req.jobId = jobId;

//     try {
//         // Get video id from url
//         const vidId = await yt.resolveURL(youtubeUrl).then(res => {return res.payload.videoId});

//         // get video info using id; access inner attr to simplify later syntax
//         const vidInfo = await yt.getInfo(vidId).then(res => {return res.basic_info});

//         // store vid metadata and start job
//         const vId = vidInfo.title.replace(/[\/\\:*?"<>|]\s/g,'_')+'-'+uId+'-'+ts;
//         const outputPath = path.join(os.tmpdir(), vId+'.mp4');
//         console.log('\nOutput Path');
//         console.log(outputPath, '\n');
//         req.jobs[jobId] = {
//             status: 'processing',
//             metadata: {
//                 videoId: vId,
//                 userId: uId,
//                 title: vidInfo.title,
//                 length: vidInfo.duration,
//                 ytId: vidInfo.id,
//                 videoPath: outputPath
//             }
//         };
        
//         // add highest res thumbnail to vid metadata
//         const thumbnail = await vidInfo.thumbnail.reduce((prev, curr) => (prev.width > curr.width) ? prev : curr);
//         req.jobs[jobId].metadata.thumbnail = thumbnail.url;

//         // confirm job start with client and close /convert req-res to process video transcription asynchronously
//         res.status(202).json({jobId, status: req.jobs[jobId].status, title: req.jobs[jobId].metadata.title });
//         next();
//     } catch (err) {
//         console.error('Error accessing YouTube video: ', err.message);
//         res.status(400).json({ error: true, message: "Error accessing YouTube video metadata.\nPlease ensure URL is correct." })
//         return;
//     }
// }