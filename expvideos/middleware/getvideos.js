/* GET movies search results. */
module.exports = function(req, res, next) {
    const selectCols = [
        'videoId', 'title', 'thumbnail',
        'length', 'ts'
    ];
    
    // 1. Return all movies IF no search terms for [title / year] 
    if (!req.query.title && !req.query.year) {
        req.db.from("videos").select(selectCols)
        .where({userId: req.user.id}).orderBy('ts')
        .then((rows) => {
            req.videos = rows;
        })
        .then(_ => {
            next();
        })
        .catch((err) => { 
            console.log(err);
            res.json({Error: true, Message: "Error in MySQL query" });
            return;
        });
    }
    else {
        req.db.from("videos").select(selectCols).where((builder) => {
            builder.where({userId: req.user.id});
            if (req.query.title) {builder.whereILike("title", `%${req.query.title}%`)};
            if (req.query.year) {builder.where("year", parseInt(req.query.year))};
        }).orderBy('tconst')
        .then((rows) => {
            req.movies = rows;
        })
        .then(_ => {
            next();
        })
        .catch((err) => { 
            console.log(err);
            res.json({Error: true, Message: "Error in MySQL query" });
            return;
        });
    }
};