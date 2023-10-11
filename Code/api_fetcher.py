import requests

API_URL = 'https://api.huuto.net/1.1/'

def make_api_request(endpoint, params=None, timeout=5):
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exception:
        print(f"Error making API request: {exception}")
        return None

def fetch_by_keyword(keyword, limit=500, timeout=5):
    params = {"words": keyword, "limit": limit}
    data = make_api_request("items", params=params, timeout=timeout)
    if data:
        items = data.get("items", [])
        return clean_data(items)
    return []

def fetch_items_by_cat_id(id, limit=500, timeout=5):
    params = {"limit": limit}
    data = make_api_request(f"categories/{id}/items", params=params, timeout=timeout)
    if data:
        items = data.get("items", [])
        return clean_data(items)
    return []

def clean_data(data):
    items_clean = []
    for item in data:
        clean_item = {
            "title": item.get("title", ""),
            "buy_now_price": item.get("buyNowPrice", 0),
            "location": item.get("location", ""),
            "postal_code": item.get("postalCode", ""),
            "current_price": item.get("currentPrice", 0)
        }
        if item.get("images"):
            clean_item["image"] = item["images"][0].get("links", {}).get("medium", "")
        items_clean.append(clean_item)
    return items_clean

item_data = fetch_by_keyword("aaltomaljakko")
furniture_data = fetch_items_by_cat_id(339)

print(furniture_data)
