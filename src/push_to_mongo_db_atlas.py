from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()
connection = os.getenv('DB_URL')

client = MongoClient(connection)

db = client.sampoDB

collection = db.item_data

# Create a unique index on the 'imageurl' field
collection.create_index([('imageurl', 1)], unique=True, partialFilterExpression={'imageurl': {'$exists': True}})


def push_many_to_mongo_db(items_array):
    try:
        collection.insert_many(items_array)
    except errors.BulkWriteError as e:
        for error in e.details['writeErrors']:
            if error['code'] == 11000:  # Duplicate key error code
                print(f"Duplicate key error: {error}")
                # Handle or log the duplicate key error as needed
            else:
                raise  # Raise other errors

def push_one_to_mongo_db(item):
    try:
        collection.insert_one(item)
    except errors.DuplicateKeyError as e:
        print(f"Duplicate key error: {e}")
        # Handle or log the duplicate key error as needed
    except errors.WriteError as e:
        print(f"Write error: {e}")
        # Handle other write errors as needed
