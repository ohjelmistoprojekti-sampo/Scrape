from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

# get numeric value for each condition
def translate_condition_to_number(kunto):
    kunto_mapping = {
        "Uusi": 5,
        "Erinomainen": 4,
        "Hyvä": 3,
        "Tyydyttävä": 2,
        "Huono": 1
    }
    return kunto_mapping.get(kunto, 0) 

def cond(link):
    url = link

    page = requests.get(url)
    soup = BS(page.content, 'html.parser')

    cond_value = None

    # Find the "Kunto:" topic and its value in the table
    topic_elem = soup.find('td', class_='topic', string='Kunto:')
    if topic_elem:
        value_elem = topic_elem.find_next('td', class_='value')
        if value_elem:
            cond_value = value_elem.get_text().strip()

    return(cond_value)
    

def ScrapeTori(num_pages=1):  # Set the number of pages you want to scrape
    # Set up Chrome driver
    driver = webdriver.Chrome()

    scraped_data = []

    for page_number in range(1, num_pages + 1):
        #change the url based on products wanted
        URL = f"https://www.tori.fi/koko_suomi/sisustus_ja_huonekalut/hyllyt_ja_sailytys?ca=18&q=sisustus%20ja%20huonekalut&cg=3020&st=s&c=3022&f=p&w=3&o={page_number}"
        driver.get(URL)
        print(URL)

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'item_row_flex')))
        except TimeoutException:
            print(f"Timeout waiting for page {page_number} to load")
            continue  # Move on to the next page if the current one times out

        page = BS(driver.page_source, "html.parser")
        products = page.find_all('a', class_='item_row_flex')

        if not products:
            print(f"No items found on page {page_number}")
            continue  # Move on to the next page if there are no items
        #find title, price and link for each product per page
        for i, products in enumerate(products, start=1):
            try:
                title = products.find('div', class_="li-title").contents[0]
                price = products.find('p', class_="list_price ineuros").contents[0].replace(" ", "")
                product_url = products.get('href')

                # Get the url for product image
                image_container = products.find('div', class_='image_container')
                image_div = image_container.find('div', class_='item_image_div') if image_container else None
                img_url = image_div.find('img', class_='item_image')['src'] if image_div and image_div.find('img', class_='item_image') else 'N/A'

                # Get the product condition
                condition = cond(product_url)
                condition_number = translate_condition_to_number(condition)

                # Create a dictionary for each item
                item_data = {
                    "title": f"{title}",
                    "price": price,
                    "imageurl": img_url,
                    "condition": condition_number
                }
                scraped_data.append(item_data)

                #follow the process
                print(f"Page {page_number}, Item {i} - Product Name: {item_data['title']}, Price: {item_data['price']}, Image Link: {item_data['imageurl']}, Condition: {item_data['condition']}")

            except Exception as e:
                print(f"Error processing item {i} on page {page_number}: {e}")
        #check amount of product scraped
        print(f'Page {page_number} - listings: {len(scraped_data)}')

    driver.quit()  # Close the browser when done
    return scraped_data

# Call the function to execute the scraping and display JSON
scraped_data = ScrapeTori(num_pages=10)  # You can adjust the number of pages as needed
print(scraped_data)
