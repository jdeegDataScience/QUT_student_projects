module.exports = function(req, res, next) {
    const BLtime = Math.floor(Date.now() / 1000);
    req.db("usersbltokens")
    .insert({email: req.user.email, BLfrom: `${BLtime}`})
    .onConflict('email')
    .merge('BLfrom')
    .then(_ => {
        next();
    });
};