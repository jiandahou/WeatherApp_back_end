const { log } = require("console");
const express=require("express");
const cors = require('cors');
const locationRoute = require("./location/location_route");
var app=express();
app.use(cors())
app.use("/location",locationRoute)
app.listen(7990,()=>{log("suncess listen")})
