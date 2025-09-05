module.exports = function(req, res, next) {
    // 1. Check email and password in req.body
    if (!req.body.email || !req.body.password) {
        res.status(400).json({ error: true, 
            message: `Request body incomplete, both email and password are required` });
        return; 
    }
    else {
        const email = req.body.email;        
        req.db
        .from("users")
        .select('*') 
        .where({email: email})
        .then((users) => {
            if (users.length !== 1) {
                req.match = false;
            }
            else {
                req.match = true;
                req.user = users[0];
            }
            next();
        })
    };
};