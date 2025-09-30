const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET;

module.exports = function(req, res, next) {
    const token = req.token;
    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        /* standardised reference for user email between middlewares */
        req.user = {};   
        req.user.email = decoded.email;
        req.db
        .from("usersbltokens")
        .select('*') 
        .where({email: req.user.email})
        .then((users) => {
            if (users.length === 0) { next(); }
            else { decoded.iat < users[0]?.BLfrom ? res.status(401).json({ error: true, message: "Invalid JWT token" }) : next();
            };
        });
    } 
    catch (e) {
        if (e.name === "TokenExpiredError") {
            res.status(401).json({ error: true, message: `JWT token has expired` });
        } else {
        res.status(401).json({ error: true, message: "Invalid JWT token" });
        }
    };
    return;
};
