module.exports = function(req, res, next) {
    // 1. Check refreshToken in req.body
    if (!req.body.refreshToken) {
        res.status(400).json({ error: true, 
            message: `Request body incomplete, refresh token required` });
        return; 
    }
    else {
        /* standardised reference for token between middlewares */
        req.token = req.body.refreshToken;
        next();
    };
};