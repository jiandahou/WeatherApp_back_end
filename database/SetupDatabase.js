const mysql = require('mysql2');
const fs = require('fs');
const content=fs.readFileSync("config.json",{encoding:"utf-8"})
const config=JSON.parse(content)
const connection=mysql.createConnection(config)
connection.query("CREATE DATABASE IF NOT EXISTS location",(err)=>(console.log(err)))
connection.query("use location",(err)=>(console.log(err)))
connection.query("CREATE TABLE IF NOT EXISTS location (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255),longtitude DECIMAL(10,6),latitude DECIMAL(10,6) )",
    (err)=>(console.log(err)))
var city=fs.readFileSync("cities.json",{encoding:"utf-8"})
var cities=JSON.parse(city)
for (const cityinfo of cities) {
    let cityinfosql={name:cityinfo.name,longtitude:cityinfo.lng,latitude:cityinfo.lat}
    connection.query("INSERT INTO location SET ?",cityinfosql,(err)=>(console.log(err)))
}
connection.end()