const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET;

module.exports = function(req, res, next) {
    // const signTime = Math.floor(Date.now() / 1000); 
    const refresh_expires = req.body?.refreshExpiresInSeconds ?? 86400;
    const refresh_exp = Math.floor(Date.now() / 1000) + refresh_expires;
    const refresh_token = jwt.sign(
        { email: req.user.email, exp: refresh_exp }, 
        JWT_SECRET
    );

    const bearer_expires = req.body?.bearerExpiresInSeconds?? 86400;
    const bearer_exp = Math.floor(Date.now() / 1000) + bearer_expires;
    const bearer_token = jwt.sign(
        { email: req.user.email, exp: bearer_exp }, 
        JWT_SECRET
    );

    res.status(200).json({
        bearerToken: {
            token: bearer_token,
            token_type: "Bearer",
            expires_in: bearer_expires
        },
        refreshToken: {
            token: refresh_token,
            token_type: "Refresh",
            expires_in: refresh_expires
        }                
    });
};