from pymongo import MongoClient
from api_fetcher import fetch_by_keyword

connection = "mongodb+srv://admin:password@sampodb.mq9vg8p.mongodb.net/" # define password

client = MongoClient(connection)

db = client.sampoDB

collection = db.item_data

data = fetch_by_keyword("aalto maljakko", 50)[0]

print(data)

# collection.insert_one(data)