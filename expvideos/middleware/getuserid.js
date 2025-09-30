module.exports = function(req, res, next) {
    req.db.from("users").select(`userId`)
    .where({email: req.user.email})
    .then((rows) => {
        req.user.id = rows[0].userId;
    })
    .then(_ => {
        next();
    })
    .catch((err) => { 
        console.log(err);
        res.json({Error: true, Message: "Error in MySQL query" });
        return;
    });
};
