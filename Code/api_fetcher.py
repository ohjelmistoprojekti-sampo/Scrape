import requests

API_URL = 'https://api.huuto.net/1.1/'

def fetch_by_keyword(keyword, timeout=5):
    response = requests.get(f"{API_URL}items?words={keyword}", timeout=timeout)

    if response.status_code == 200:
        data = response.json()

    items = data["items"]
    return clean_data(items)

def clean_data(data):
    items_clean = []
    for item in data:
        clean_item = {
            "title": item["title"],
            "buy_now_price": item["buyNowPrice"],
            "location": item["location"],
            "postal_code": item["postalCode"],
            "image": item["images"][0].get("links").get("medium")
        }
        items_clean.append(clean_item)
    return items_clean

item_data = fetch_by_keyword("aaltomaljakko")
print(item_data)
