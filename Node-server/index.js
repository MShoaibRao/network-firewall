const express = require('express')
const mongoose = require('mongoose');
const cors = require('cors')
const { UserModel, blockedDevicesModel, deviceReportModel }  = require('./models/Users');
const { pieChartModel, barChartModel, lineChartModel } = require('./models/Charts');
// const { firstRowModel } = require('./models/Dasboard');
const firstRowModel = require('./models/Dashboard')
const { exec } = require('child_process');
const appDecodeModel  = require('./models/Decodes');
const { blockIPs } = require('./models/Services');
const app =  express()
app.use(cors())
app.use(express.json())

//db connection
mongoose.connect("mongodb://127.0.0.1:27017/IntelliFirewall")


//Manage devices
app.get('/getUser', (req, res) => {
    UserModel.find()
        .then(Packet => {
            console.log("HERE" , Packet); // Print data to console
            res.json(Packet);
        })
        .catch(err => res.json(err));
})

//----------------------------------------------------------

//Device report
app.get('/getDeviceReport', (req, res) => {
    deviceReportModel.find()
    .then(divice_reports => {
        console.log("here ", divice_reports);
        res.json(divice_reports)
    })
    .catch(err => res.json(err));
})

//----------------------------------------------------------

app.get('/getBlockedDevices', (req, res) => {
    blockedDevicesModel.find()
    .then(blocked_devices => {
        console.log("here ", blocked_devices);
        res.json(blocked_devices)
    })
    .catch(err => res.json(err));
})

//-----------------------------------------------------------

app.get('/getPieChart', (req, res) => {
    pieChartModel.find()
    .then(pie_charts => {
        console.log("here ", pie_charts);
        res.json(pie_charts)
    })
    .catch(err => res.json(err));
})

//-----------------------------------------------------------

app.get('/getBarChart', (req, res) => {
    barChartModel.find()
    .then(bar_chart => {
        console.log("here ", bar_chart);
        res.json(bar_chart)
    })
    .catch(err => res.json(err));
})


// ----------------------------------------------------------------

app.get('/getlineChart', (req, res) => {
    lineChartModel.find()
    .then(line_chart => {
        console.log("here ", line_chart);
        res.json(line_chart)
    })
    .catch(err => res.json(err));
})


//---------------------------------------------------------------
//Dashboard
app.get('/firstRowItems', (req, res) => {
    
    firstRowModel.find({}, { _id: 0 })
    .then(dasboard_itmes => {
        // console.log("here ", dasboard_itmes);
        res.json(dasboard_itmes)
    })
    .catch(err => res.json(err));
})





////////////////////////////////////////////////////// Post Api ////////////////////////////////////////
app.get('/api/block-ips', (req,res) => {
    res.send('GET request received at /api/block-ips');
})
app.post('/api/block-ips', async (req, res) => {
    try {
        const { id, app } = req.body;
        console.log('Received ID:', id);
        console.log('Received App:', app);

        // Your logic to block IPs associated with the provided id and app
        // Example: Assume you have a function `blockIPs` that handles the blocking logic.
        const blockingResult = await blockIPs(id, app);

        // If the IP blocking operation is successful, return success message
        res.json({ message: 'IPs have been successfully blocked.' });
    } catch (error) {
        console.error('Error blocking IPs:', error);
        // Return an error status code and message to the client
        res.status(500).json({ error: 'Error blocking IPs' });
    }
});




















app.listen(5002, () => {
    console.log("server is running")

})