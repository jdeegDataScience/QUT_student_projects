const ytdl = require('ytdl-core');
const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const path = require('path');
const os = require('os');


module.exports = function(req, res, next) {
    ffmpeg.setFfmpegPath(ffmpegPath);

    const ts = Date.now().toString();
    req.body.video.id = req.body.video.title.replace(/\s/g,'')+'-'+ts;

    const youtubeUrl = req.body.video.url;
    const tmpName = req.body.video.title.replace(/\s/g,'')+'-'+ts+'.mp4';
    const outputPath = path.join(os.tmpdir(), tmpName);
    const format = 'mp4';

    try {
        const videoStream = ytdl(youtubeUrl, { quality: 'highestvideo' }); // Or 'highestaudio' for just audio
        ffmpeg(videoStream)
        .toFormat(format)
        .on('error', (err) => {
            console.error('Error during conversion:', err);
        })
        .save(outputPath)
        .on('end', () => {
            // console.log(`Conversion complete! File saved to: ${outputPath}`);
            req.convertedVid = outputPath;
            next();
        });
    } catch (error) {
        console.error('Error downloading YouTube video:', error);
        res.status(503).json({ error: true, message: "Error converting YouTube video." })
        return;
    }
}
// Example usage:
// const youtubeVideoUrl = 'YOUR_YOUTUBE_VIDEO_URL'; // Replace with the actual YouTube URL
// const outputFilePath = 'output.mp4'; // Or 'output.mp4' for video
// convertYouTubeVideo(youtubeVideoUrl, outputFilePath, 'mp3'); // Or 'mp4' for video