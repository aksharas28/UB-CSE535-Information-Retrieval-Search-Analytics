# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:34:43 2019

@author: vignajeeth
"""


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import json
from tqdm import tqdm
import topic_modelling
import emoji
from pymongo import MongoClient

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

# Connection to the MongoDB Server
mongoClient = MongoClient('localhost:27017')
db = mongoClient.ir
collection = db.result
processed = topic_modelling.ground_truth()
translator = Translator()
analyzer = SentimentIntensityAnalyzer()

def get_processed_record(entry):
    print("Current custom id:", entry["custom_id"])
    entry['translated_sentence'] = entry["tweet_text"]
    if entry["lang"] == "hi" or entry["lang"] == "pt":
        entry['translated_sentence'] = translator.translate(remove_emoji(entry['tweet_text'])).text

    entry['sentiment'] = analyzer.polarity_scores(entry['translated_sentence'])["compound"]

    entry['topic'] = topic_modelling.topic(entry['translated_sentence'], processed)
    return entry

if __name__ == "__main__":
    write_collection = db.processed
    # cursor = collection.find({"custom_id": {"$gt": 9370}})
    cursor = collection.find({"custom_id": {"$gt": 30000, "$lt": 40001}})

    for document in cursor:
        result = get_processed_record(document)
        write_collection.insert(result)

