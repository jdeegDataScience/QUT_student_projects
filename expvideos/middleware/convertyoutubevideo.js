// // const { Innertube, UniversalCache, Utils } = require('youtubei.js');
// const { createWriteStream } = require('fs');
// const { ytPromise } = require('./youtubestream');

// // const ffmpeg = require('fluent-ffmpeg');
// // const ffmpegPath = require('ffmpeg-static');

// module.exports = async function(req, res, next) {
//     const yt = await ytPromise;
//     const ytId = req.jobs[req.jobId].metadata.ytId;
//     const ytVid = "https://www.youtube.com/watch?v=" + ytId;
//     const format = 'mp4';
//     const outputPath = req.jobs[req.jobId].metadata.videoPath;

//     console.log(ytId);
//     console.log(ytVid);

//     // ffmpeg.setFfmpegPath(ffmpegPath);

//     try {
        
//         const stream = await yt.download(ytVid, {
//             type: 'video+audio', // audio, video or video+audio
//             quality: 'best', // best, bestefficiency, 144p, 240p, 480p, 720p and so on.
//             format: format, // media container format,
//             client: 'WEB'
//         });


//         console.log(`Downloading ${req.jobs[req.jobId].metadata.title} (${ytId})`);

//         // if (!existsSync(dir)) {
//         //     mkdirSync(dir);
//         // };

//         const file = createWriteStream(outputPath);

//         stream.pipe(file);

//         file.on('error', (err) => {
//             console.error('Error during conversion:', err.message);
//             file.destroy(); // cleanup, release file descriptor
//             req.jobs[req.jobId].status = 'error';
//             req.jobs[req.jobId].error = err.message;
//             req.sendToUser(
//                 req.jobs[req.jobId].metadata.userId, 'job-error',
//                 { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, error: err.message }
//             );
//         });

//         file.on('finish', () => {
//             console.log(`Conversion complete! File saved to: ${outputPath}`);
//             req.jobs[req.jobId].status = 'complete';
//             req.sendToUser(
//                 req.jobs[req.jobId].metadata.userId, 'job-complete',
//                 { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, downloadLink: outputPath }
//             );
//         });


//         // for await (const chunk of Utils.streamToIterable(stream)) {
//         //     file.write(chunk)
//         // };
//         // Ensure file is fully flushed
//         // await new Promise((resolve, reject) => {
//         //     file.on('error', reject);
//         //     file.end(resolve);
//         // });


//         /* const videoStream = ytdl(youtubeUrl, { quality: 'highestvideo' }); // Or 'highestaudio' for just audio
//         ffmpeg(videoStream)
//         .toFormat(format)
//         .on('error', (err) => {
//             console.error('Error during conversion:', err);
//             req.jobs[req.jobId].status = 'error';
//             req.jobs[req.jobId].error = err.message;
//             req.sendToUser(
//                 req.jobs[req.jobId].metadata.userId, 'job-error',
//                 { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, error: err.message }
//             );
//             return;
//         })
//         .save(outputPath)
//         .on('end', () => {
//             console.log(`Conversion complete! File saved to: ${outputPath}`);
//             req.jobs[req.jobId].status = 'complete';
//             req.sendToUser(
//                 req.jobs[req.jobId].metadata.userId, 'job-complete',
//                 { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, downloadLink: outputPath }
//             );
//             return;
//         }); */
//     } catch (err) {
//         console.error('Error initialising upload of YouTube video: ', req.jobs[req.jobId].metadata.title);
//         console.error('Error: ', err);
//         // Clean up incomplete file if it exists
//         // try { file && file.destroy(); } catch (e) {}
//         req.jobs[req.jobId].status = 'error';
//         req.jobs[req.jobId].error = err.message;
//         req.sendToUser(
//             req.jobs[req.jobId].metadata.userId, 'job-error',
//             { jobId: req.jobId, status: req.jobs[req.jobId].status, title: req.jobs[req.jobId].metadata.title, error: err.message }
//         );
//     }
//     return;
// }
// // Example usage:
// // const youtubeVideoUrl = 'YOUR_YOUTUBE_VIDEO_URL'; // Replace with the actual YouTube URL
// // const outputFilePath = 'output.mp4'; // Or 'output.mp4' for video
// // convertYouTubeVideo(youtubeVideoUrl, outputFilePath, 'mp3'); // Or 'mp4' for video