from api_fetcher import fetch_by_keyword, fetch_items_by_cat_id
from push_to_mongo_db_atlas import push_many_to_mongo_db, push_one_to_mongo_db
from IkeaScrapeCategoryAllTheProducts import scrape_ikea
from HuutoNet_Scrape import scrape_huuto
from ToriScrapeSyötteellä import scrapeTori


if __name__ == "__main__":
    huuto_base_url = "https://www.huuto.net/haku/category/339"
    huuto_data = scrape_huuto(huuto_base_url)
    ikea_data = scrape_ikea()
    tori_data = scrapeTori()
    
    push_many_to_mongo_db(huuto_data)
    push_many_to_mongo_db(ikea_data)
    push_many_to_mongo_db(tori_data)
    