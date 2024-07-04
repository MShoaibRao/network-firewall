const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    _id: String,
    IP: String,
    Url: String,
    Mac: String,
    Port: String,
})

//device report
const deviceReportSechema = new mongoose.Schema({
    connect_time: String,
    disconnect_time: String,
    ip: String,
    mac: String,
    status: String
})

//Blocked Device
const blockedDevicesSchema = new mongoose.Schema({
    _id: String,
    IP: String,
    Mac: String,
    Date: String

})


//moduling
const UserModel = mongoose.model("Packet", UserSchema)
const deviceReportModel = mongoose.model("divice_reports", deviceReportSechema)
const blockedDevicesModel = mongoose.model("blocked_devices", blockedDevicesSchema)


//exporting
module.exports = 
module.exports = 
module.exports = 

module.exports = {
    UserModel,
    deviceReportModel,
    blockedDevicesModel
};