from api_fetcher import fetch_by_keyword, fetch_items_by_cat_id
from push_to_mongo_db_atlas import push_many_to_mongo_db, push_one_to_mongo_db

if __name__ == "__main__":
    items = fetch_items_by_cat_id(339)
    push_many_to_mongo_db(items)
    