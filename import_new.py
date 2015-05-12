import json
import glob
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.sample
collection = db.test

f = open('sample.osm.json', 'r')

for line in f.read().split("\n"):
      if line:
            try:
              lineJson = json.loads(line)
            except (ValueError, KeyError, TypeError) as e:
              pass
      else:
         postid = collection.insert(lineJson)
         print 'inserted with id: ' , postid

f.close()
