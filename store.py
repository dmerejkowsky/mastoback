import pymongo

client = pymongo.MongoClient()

db = client.mastoback

collection = db.toots

collection.insert_one({
   "text": "hello, world"
})
