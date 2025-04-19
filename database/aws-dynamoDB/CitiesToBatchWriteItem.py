import json
import re
def convert_city_to_dynamodb_format(city):
    return {
        "PutRequest": {
            "Item": {
                "name": {"S": city["name"]},
                "lat": {"N": city["lat"]},
                "lng": {"N": city["lng"]},
                "country": {"S": city["country"]},
                "admin1": {"S": city["admin1"]},
                "admin2": {"S": city["admin2"]}
            }
        }
    }
with open("../cities.json","r",encoding="utf-8") as f:
    cities=json.load(f)
    batchWriteItem=[convert_city_to_dynamodb_format(city) for city in cities]
with open("citiesBatchWriteItem.json","w",encoding="utf-8") as f:
    json.dump(batchWriteItem,f,indent=2,ensure_ascii=False)