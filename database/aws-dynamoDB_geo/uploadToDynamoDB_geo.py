import json
import boto3
import geohash2
ddb = boto3.resource("dynamodb", region_name="ap-southeast-2")
table = ddb.Table("Weather_app_location_geo")
GEO_PRECISION = 5
def put_city(city):
    lat = float(city["lat"])
    lng = float(city["lng"])
    geo = geohash2.encode(lat, lng, precision=GEO_PRECISION)
    item = {
        "hashKey": geo,
        "rangeKey": city["name"],
        "geoHash": geo,
        "latitude": str(lat),
        "longitude": str(lng),
        "country": city["country"],
        "admin1": city.get("admin1",""),
        "admin2": city.get("admin2","")
    }
    table.put_item(Item=item)
    print("Wrote:", city["name"])
with open("../cities.json","r",encoding="utf-8") as f:
    cities = json.load(f)
    for c in cities:
        put_city(c)
    print("All done!")