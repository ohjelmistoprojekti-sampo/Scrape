from pymongo import MongoClient

connection = "mongodb+srv://admin:password@sampodb.mq9vg8p.mongodb.net/" # define password

client = MongoClient(connection)

db = client.sampoDB

collection = db.item_data

def push_many_to_mongo_db(items_array):
    collection.insert_many(items_array)


def push_one_to_mongo_db(item):
    collection.insert_one(item)
