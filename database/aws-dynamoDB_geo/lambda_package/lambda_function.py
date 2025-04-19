import json
import math
import geohash2
import boto3
from boto3.dynamodb.conditions import Key
TABLE_NAME = "Weather_app_location_geo"
PRECISION  = 5
ddb   = boto3.resource("dynamodb", region_name="ap-southeast-2")
table = ddb.Table(TABLE_NAME)
def haversine(lat1, lon1, lat2, lon2):
    to_rad = math.radians
    R = 6371e3
    dlat = to_rad(lat2 - lat1)
    dlon = to_rad(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(to_rad(lat1))*math.cos(to_rad(lat2))*
         math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
DIRS = {
  "N":  ("top",),
  "S":  ("bottom",),
  "E":  ("right",),
  "W":  ("left",),
  "NE": ("top","right"),
  "NW": ("top","left"),
  "SE": ("bottom","right"),
  "SW": ("bottom","left")
}
def get_neighbors(g):
    out = []
    for steps in DIRS.values():      
        cur = g
        for s in steps:
            cur = geohash2.adjacent(cur, s)  
        out.append(cur)
    return out
def find_nearest(lon, lat):
    center    = geohash2.encode(lat, lon, PRECISION)
    neighbors = get_neighbors(center) + [center]
    best, best_d = None, float("inf")

    for p in neighbors:
        resp = table.query(
            KeyConditionExpression=Key("hashKey").eq(p)
        )
        for item in resp.get("Items", []):
            try:
                lat2 = float(item["latitude"])
                lon2 = float(item["longitude"])
            except:
                continue
            d = haversine(lat, lon, lat2, lon2)
            if d < best_d:
                best, best_d = item, d

    return best, best_d
def lambda_handler(event, context):
    params = event.get("pathParameters") or {}
    lon_s  = params.get("longtitude")
    lat_s  = params.get("latittude")
    try:
        lon = float(lon_s)
        lat = float(lat_s)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"status":"error","message":"Invalid path parameters"})
        }

    item, dist = find_nearest(lon, lat)
    if not item:
        body = {"status":"fail","value":None}
        code = 404
    else:
        item["distance"] = dist
        body = {"status":"success","value":item}
        code = 200
    return {
        "statusCode": code,
        "headers": {"Content-Type":"application/json"},
        "body": json.dumps(body, ensure_ascii=False)
    }