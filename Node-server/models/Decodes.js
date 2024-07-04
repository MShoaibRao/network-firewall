const mongoose = require('mongoose');

const appDecodeSchema = new mongoose.Schema({
    id: String,
    app: String,
    ip: String,
    url: String,
});




const appDecodeModel = mongoose.model("app_decodes", appDecodeSchema)



//exporting
module.exports = {
    appDecodeModel
};