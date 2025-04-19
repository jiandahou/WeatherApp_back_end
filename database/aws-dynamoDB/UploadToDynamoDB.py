import boto3
import json
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Weather_app_location')
with open('../cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print("Key schema:", table.key_schema)
print("Attribute definitions:", table.attribute_definitions)
success = 0
failed = 0

with table.batch_writer() as batch:
    for idx, item in enumerate(data, start=1):
        name = item["name"]
        try:
            batch.put_item(item)
            success += 1
        except Exception as e:
            failed += 1
            # 把 name 原始和 repr(name) 都打印出来：
            print(f"❌ Failed to insert item {idx}: name={name!r}, repr={repr(name)}, error={e}")
            continue

print(f"✅ Done. Success={success}, Failed={failed}")