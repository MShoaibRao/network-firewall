const mongoose = require('mongoose');

const pieChartSchema = new mongoose.Schema({
    id: String,
    lable: String,
    value: Number
});



const barChartSchema = new mongoose.Schema({
    id: String,
    DeviceMAC: String,
    Facebook_kbs: Number,
    Google_kbs: Number,
    YouTube_kbs: Number,
    local_kbs: Number
});



const lineChartSchema = new mongoose.Schema({
    Line: String,
    data: [
        {
            x:String,
            y: Number
        }

    ]
    
})

// data: [
//         {
//             x1:String,
//             y1: Number
//         },
//         {
//             x2:String,
//             y2: Number
//         },
//         {
//             x3:String,
//             y3: Number
//         },
//         {
//             x4:String,
//             y4: Number
//         },
//         {
//             x5:String,
//             y5: Number
//         },
//         {
//             x6:String,
//             y6: Number
//         },
//         {
//             x7:String,
//             y7: Number
//         },
//         {
//             x8:String,
//             y8: Number
//         },
//         {
//             x9:String,
//             y9: Number
//         },
//         {
//             x10:String,
//             y10: Number
//         },
//         {
//             x11:String,
//             y11: Number
//         },
//         {
//             x12:String,
//             y12: Number
//         }

//     ]

//moduling
const pieChartModel = mongoose.model("pie_charts", pieChartSchema)
const barChartModel = mongoose.model("bar_charts", barChartSchema)
const lineChartModel = mongoose.model("line_charts", lineChartSchema)



//exporting
module.exports = {
    pieChartModel,
    barChartModel,
    lineChartModel
};