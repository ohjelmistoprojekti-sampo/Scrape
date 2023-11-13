import requests
from bs4 import BeautifulSoup
import re

def extract_numeric_value(s):
    # Use regular expression to extract numeric values
    numeric_part = re.search(r'\b\d+(\.\d+)?\b', s)
    return float(numeric_part.group()) if numeric_part else None

# Translates the condition to the given number as in the database
def translate_condition_to_number(condition):
    condition_mapping = {
        "Uusi": 5,
        "Uudenveroinen": 4,
        "Hyvä": 3,
        "Tyydyttävä": 2,
        "Heikko": 1
    }

    return condition_mapping.get(condition, 0)  # Default to 0 if the condition is not in the mapping

def scrape_huuto(base_url):
    data_list = []  # Create a list to store dictionaries for each item

    # Scrape the first page
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="search-container")

    job_elements = results.find_all("div", class_="item-card__title")
    hinta = results.find_all("div", class_="item-card__price")
    nimi = results.find_all("div", class_="item-card__title")
    kunto = results.find_all("div", class_="item-card__condition")
    images = results.find_all("img", class_="item-card__image")

    for hinta_elem, nimi_elem, kunto_elem, image_elem in zip(hinta, nimi, kunto, images):
        hinta_str = hinta_elem.get_text().replace(" ", "").replace("\n", "").replace("€", "").replace(",", "")
        nimi_str = nimi_elem.get_text().strip()
        kunto_str = kunto_elem.get_text().replace(" ", "").replace("\n", "")
        image_url = image_elem['src']

        hinta_float = extract_numeric_value(hinta_str)
        kunto_number = translate_condition_to_number(kunto_str)

        # Check if the image URL is already in the list
        if not any(item['imageurl'] == image_url for item in data_list):
            # Create a dictionary for each item
            item_data = {
                    "title": nimi_str,
                    "price": hinta_float,
                    "condition": kunto_number,
                    'imageurl': image_url
                }

            # Append the dictionary to the list
            data_list.append(item_data)

    # Find the total number of pages from the pagination section
    pagination_section = soup.find("ul", class_="show-for-medium-up")
    total_pages_elem = [elem for elem in pagination_section.find_all("a") if elem.text.strip().isdigit()]
    total_pages = int(total_pages_elem[-1].text) if total_pages_elem else 1
    print(total_pages)

    # Iterate through all pages and scrape
    for i in range(2, total_pages + 1):
        page_url = f"https://www.huuto.net/haku/page/{i}/category/339"
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(id="search-container")

        # Search all the different data from divs
        job_elements = results.find_all("div", class_="item-card__title")
        hinta = results.find_all("div", class_="item-card__price")
        nimi = results.find_all("div", class_="item-card__title")
        kunto = results.find_all("div", class_="item-card__condition")
        images = results.find_all("img", class_="item-card__image")

        # Loop trough the scraped elements and strip them and only get the needed data
        for hinta_elem, nimi_elem, kunto_elem, image_elem in zip(hinta, nimi, kunto, images):
            hinta_str = hinta_elem.get_text().replace(" ", "").replace("\n", "").replace("€", "").replace(",", "")
            nimi_str = nimi_elem.get_text().strip()
            kunto_str = kunto_elem.get_text().replace(" ", "").replace("\n", "")
            image_url = image_elem['src']

            # Check if the image URL is already in the list
            if not any(item['imageurl'] == image_url for item in data_list):
                # Update hinta_float and kunto_number for subsequent pages
                hinta_float = extract_numeric_value(hinta_str)
                kunto_number = translate_condition_to_number(kunto_str)

                # Create a dictionary for each item
                item_data = {
                    "title": nimi_str,
                    "price": hinta_float,
                    "condition": kunto_number,
                    'imageurl': image_url
                }

                # Append the dictionary to the list
                data_list.append(item_data)
                
    print(len(data_list))
    return data_list

if __name__ == "__main__":
    # Specify the base URL
    base_url = "https://www.huuto.net/haku/category/339"
    scraped_data = scrape_huuto(base_url)
    
    # Print the list of dictionaries
    for item in scraped_data:
        print(item)
    print(len(scraped_data))
