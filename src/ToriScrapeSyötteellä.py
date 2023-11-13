from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import requests
from urllib.parse import quote

def kunto(linkki):
    url = linkki

    page = requests.get(url)
    soup = BS(page.content, 'html.parser')

    kunto_value = None

    # Find the "Kunto:" topic and its value in the table
    topic_elem = soup.find('td', class_='topic', string='Kunto:')
    if topic_elem:
        value_elem = topic_elem.find_next('td', class_='value')
        if value_elem:
            kunto_value = value_elem.get_text().strip()

    return(kunto_value)
    

def ScrapeTori(num_pages=5):  # Set the number of pages you want to scrape
    # Set up Chrome driver
    driver = webdriver.Chrome()

    scraped_data = []

    for page_number in range(1, num_pages + 1):
        URL = f"https://www.tori.fi/koko_suomi/sisustus_ja_huonekalut/sohvat_ja_nojatuolit?ca=18&q=sisustus%20ja%20huonekalut&cg=3020&st=s&c=3025&w=3&o={page_number}"
        driver.get(URL)
        print(URL)
        
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'item_row_flex')))
        except TimeoutException:
            print(f"Timeout waiting for page {page_number} to load")
            continue  # Move on to the next page if the current one times out

        sivu = BS(driver.page_source, "html.parser")
        tuotteet = sivu.find_all('a', class_='item_row_flex')

        if not tuotteet:
            print(f"No items found on page {page_number}")
            continue  # Move on to the next page if there are no items

        for i, tuotteet in enumerate(tuotteet, start=1):
            try:
                id = tuotteet.get('id')
                title = tuotteet.find('div', class_="li-title").contents[0]
                price = tuotteet.find('p', class_="list_price ineuros").contents[0].replace(" ", "")
                tuote_linkki = tuotteet.get('href')

                # Check for the updated structure
                image_container = tuotteet.find('div', class_='image_container')
                image_div = image_container.find('div', class_='item_image_div') if image_container else None
                kuva_linkki = image_div.find('img', class_='item_image')['src'] if image_div and image_div.find('img', class_='item_image') else 'N/A'

                # Get the product condition
                condition = kunto(tuote_linkki)

                # Create a dictionary for each item
                item_data = {
                    "Product Name": f"{title} ({id})",
                    "Price": price,
                    "Image Link": kuva_linkki,
                    "Condition": condition
                }
                scraped_data.append(item_data)

                print(f"Page {page_number}, Item {i} - Product Name: {item_data['Product Name']}, Price: {item_data['Price']}, Image Link: {item_data['Image Link']}, Condition: {item_data['Condition']}")

            except Exception as e:
                print(f"Error processing item {i} on page {page_number}: {e}")

        print(f'Page {page_number} - listings: {len(scraped_data)}')

    driver.quit()  # Close the browser when done
    return scraped_data

# Call the function to execute the scraping and display JSON
scraped_data = ScrapeTori(num_pages=5)  # You can adjust the number of pages as needed

# Optionally, you can convert the scraped data to JSON

print(scraped_data)
