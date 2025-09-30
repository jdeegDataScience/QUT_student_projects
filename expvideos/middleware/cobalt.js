const CobaltAPI = require("cobalt-api");


module.exports = async function(req, res, next) {
    const cobalt = new CobaltAPI(req.body.url);

    cobalt.sendRequest()
    .then((response) => {
        if (response.status) {
            console.log("Download successful", response.data);
            res.status(200).json({data: response.data});
        } else {
            console.log("Download failed", response.text);
        }
    })
    .catch((err) => {
        console.error("Error:", err)
        res.status(400).json({error: true, message: err.message});
    });
}