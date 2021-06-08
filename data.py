import pymongo

cluster=pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["learning_challenge"]
collection = db["Topics_Learnt"]

for x in collection.find():
    print(x) 