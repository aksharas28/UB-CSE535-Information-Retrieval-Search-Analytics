import json, os, re, random
from pymongo import MongoClient

def my_replace(match):
    return "\"#" + match.group()[1:]

def replace_color(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        result_string = f.read()

    result_string = re.sub("\"(0x|0X)?[a-fA-F0-9]{6}\"", my_replace, result_string)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(result_string)

def write_to_elastic(result):
    print(len(result))
    with open("temp.json", "w") as f:
        for entry in result:
            json.dump(entry, f)
            f.write("\n")

    replace_color("temp.json")

    os.system("curl -XPOST -H \"Content-Type: application/x-ndjson\" 34.221.119.120:9200/_bulk --data-binary @temp.json")


# Connection to the MongoDB Server
mongoClient = MongoClient('localhost:27017')
db = mongoClient.ir
collection = db.result
cursor = collection.find({"custom_id": {"$lt": 30001}})

result = []
count = 0

for document in cursor:
    del(document['_id'])
    result.append({ "index" : { "_index" : "tweets", "_id" : document["custom_id"] } })
    result.append(document)
    count += 1
            
    if count % 1000 == 0:
        write_to_elastic(result)
        result = []

write_to_elastic(result) 
