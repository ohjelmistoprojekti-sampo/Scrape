import requests
from bs4 import BeautifulSoup
import time

data_list = []

search_term = input("Tuotteen nimi: ")
url = f'https://www.ikea.com/fi/fi/search/?q={search_term}'
page = requests.get(url)

# Check if the request was successful
if page.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(page.content, 'html.parser')
else:
    print(f"Failed to retrieve the page. Status code: {page.status_code}")
    exit()
time.sleep(2)
results = soup.find(class_="plp-price-module__information")
print(results)

if results:
    name_elements = results.find_all("h3", class_="plp-price-module__name")

    for name_elem in name_elements:
        data_list.append(name_elem.get_text())

    print(data_list)
else:
    print("No results found.")
