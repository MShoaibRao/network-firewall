const mongoose = require('mongoose');

const firstRowSchema = new mongoose.Schema({
    Traffic_Speed: Number,
    Unknown_traffic: Number,
    Connected_devices: Number,
    Vpn_traffic: Number
});



// Moduling
const firstRowModel = mongoose.model("dasboard_items", firstRowSchema)



//Exporting
module.exports = firstRowModel