import json, os, re, random
from pymongo import MongoClient

# Connection to the MongoDB Server
mongoClient = MongoClient('localhost:27017')
db = mongoClient.ir
collection = db.tweets

tweets_set = set()

def clean_tweets(text):
    return re.sub('@[^\s]+','',text)

def my_replace(match):
    return "\"#" + match.group()[1:]

def replace_color(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        result_string = f.read()

    result_string = re.sub("\"(0x|0X)?[a-fA-F0-9]{6}\"", my_replace, result_string)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(result_string)


def dedup_tweets():

    result = []
    cursor = collection.find({})
    count =0

    for document in cursor:
        tweet_id = document['id']

        if tweet_id not in tweets_set:

            tweets_set.add(tweet_id)
            del(document['_id'])
            if 'extended_entities' in document:
                del(document['extended_entities'])
            if 'text' in document:
                document['tweet_text'] = document['text']
                del(document['text'])
            
            if 'full_text' in document:
                document['tweet_text'] = document['full_text']
                del(document['full_text'])
            document['tweet_lang'] = document['lang']
            
            # Make language based keys
            if 'text_en' not in document:
                if document['lang'] == 'en':
                    document['text_en'] = document['tweet_text']
                else:
                    document['text_en'] = ""
            
            if 'text_hi' not in document:
                if document['lang'] == 'hi':
                    document['text_hi'] = document['tweet_text']
                else:
                    document['text_hi'] = ""
            
            if 'text_pt' not in document:
                if document['lang'] == 'pt':
                    document['text_pt'] = document['tweet_text']
                else:
                    document['text_pt'] = ""
            document['clean_text'] = clean_tweets(document['tweet_text'])
            # result.append({ "index" : { "_index" : "tweets", "_id" : count } })
            document["custom_id"] = count
            result.append(document)    
            count += 1
            
            # if count % 1000 == 0:
                # break
                # write_to_elastic(result)
                # result = []

    # write_to_elastic(result)
    write_to_mongo(result)
    
def write_to_mongo(result):
    collection = db.result
    collection.insert(result)

def write_to_elastic(result):
    print(len(result))
    with open("temp.json", "w") as f:
        for entry in result:
            json.dump(entry, f)
            f.write("\n")

    replace_color("temp.json")

    os.system("curl -XPOST -H \"Content-Type: application/x-ndjson\" localhost:9200/_bulk --data-binary @temp.json")


dedup_tweets()


# # Randomize inputs
# random_result = []
# for i in range(10000):
#     index = random.randrange(0, 300000)
#     random_result.append(result[index])

# with open("data_random.json", "w") as f:
#     for entry in random_result:
#         json.dump(entry, f)
#         f.write("\n")

# replace_color("data_random.json")




