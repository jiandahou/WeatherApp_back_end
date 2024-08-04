const mysql = require('mysql2');
const fs = require('fs');
const content=fs.readFileSync("database/config.json",{encoding:"utf-8"})
const config=JSON.parse(content)
const connection=mysql.createConnection(config)
connection.query("use location",(err)=>(console.log(err)))
function getLocationinfoByname(name,callback){
    connection.query("SELECT * from location where name=?",[name],(err,result,fields)=>{
        var re={}
        if(err){
            re= {
                status:"error",
                message:err,
            }
        }
        else if(result.length==0){
            re= {
                status:"fail",
                value:result
            }
        }
        else{
            re= {
                status:"success",
                value:result[0]
            }
        }
        callback(re)
})
}
function  getLocationinfoByLongtitudeAndLatitude(longtitude,latittude,callback){
    var re={}
    var sql=mysql.format("SELECT id,name,longtitude,latitude,ST_Distance_Sphere(point(longtitude, latitude),point(?, ?)) AS distance from location order by distance ASC limit 10",[longtitude,latittude])
    console.log(sql)
    connection.query("SELECT id,name,longtitude,latitude,ST_Distance_Sphere(point(longtitude, latitude),point(?, ?)) AS distance from location order by distance ASC limit 10",[longtitude,latittude],(err,result,fields)=>{
        if(err){
            re= {
                status:"error",
                message:err,
            }
        }
        else if(result.length==0){
            re= {
                status:"fail",
                value:result
            }
        }
        else{
            re= {
                status:"success",
                value:result[0]
            }
        }
        callback(re)
    })
}
module.exports={
    getLocationinfoByname,
    getLocationinfoByLongtitudeAndLatitude
}