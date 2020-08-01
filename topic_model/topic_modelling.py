# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:12:50 2019

@author: vignajeeth
"""



from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


def process(raw_data):
    #    data=raw_data.split()
    # specials
    data = [re.sub('\W+', '', w) for w in raw_data]
    # to lower
    data = [w.lower() for w in data]
    # stop words
    stop = set(stopwords.words('english'))
    data = [word for word in data if word not in stop]
    # stemming
    ps = PorterStemmer()
    data = [ps.stem(w) for w in data]
    return (data)


def ground_truth():
    raw = {}

    f = open("crime.txt", "r")
    raw['crime'] = f.read()

    f = open("education.txt", "r")
    raw['education'] = f.read()

    f = open("environment.txt", "r")
    raw['environment'] = f.read()

    f = open("politics.txt", "r")
    raw['politics'] = f.read()

    processed = {}
    for i in raw:
        processed[i] = set(process(raw[i].split()))

    for i in processed:
        for j in processed:
            if i != j:
                processed[i] -= processed[j]
    return processed


def topic(tweet, processed):
    #tweet='Mortgage rates have fallen. If you’re paying a mortgage – even and especially if you’ve recently refinanced – you should consider locking in a lower rate and refinancing with Quicken Loans. Think of what you could save! (Don’t worry - were experts!)'
    tknzr = TweetTokenizer()
    data = tknzr.tokenize(tweet)
    new_data = process(data)
    new_data = list(filter(None, new_data))

    counter = {}
    for i in processed:
        for j in new_data:
            if j in processed[i]:
                counter[i] = counter.get(i, 0) + 1

    try:
        maxi = max(counter.values())
    except ValueError:
        return 'Neutral'
    max_count = 0
    for i in counter.values():
        if maxi == i:
            max_count += 1

    if max_count > 1:
        return 'Neutral'
    else:
        return max(counter.items(), key=lambda x: x[1])[0]


if __name__ == "__main__":
    processed = ground_truth()

# import pickle

# fp = open("hindi_to_eng.pkl", "rb")  # Input your dataset
# x_data = pickle.load(fp)

# ans = []
# for i in x_data:
#     ans.append(topic(i, processed))
