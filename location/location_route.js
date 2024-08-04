const express=require("express")
const locationsql=require("../database/location")
const locationRoute=express.Router()
locationRoute.get("/name/:name",(req,res)=>{
locationsql.getLocationinfoByname(req.params.name,(result)=>(res.send(result)));})
module.exports=locationRoute;
locationRoute.get("/:longtitude/:latitude",(req,res)=>{
    locationsql.getLocationinfoByLongtitudeAndLatitude(req.params.longtitude,req.params.latitude,(result)=>(res.send(result)))
})
locationRoute.post("/:longtitude/:latitude",(req,res)=>{console.log(req.params.longtitude);
    console.log(req.params.latitude);})