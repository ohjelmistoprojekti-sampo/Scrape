import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def setUp():
    driver = webdriver.Chrome()
    driver.get('https://www.tori.fi/koko_suomi?q=tuoli&cg=0&w=3')

def accept_cookie_consent(self):
        try:
            # Wait for the cookie consent button to be clickable
           consent_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Hyväksy kaikki evästeet' and @class='message-component message-button no-children focusable sp_choice_type_11 last-focusable-el']"))
            )
           self.driver.execute_script("arguments[0].click();", consent_button)
        except:
            # If the button is not found or not clickable, just proceed
            pass

def test_scrape_tori(self):
        driver = self.driver  
        self.accept_cookie_consent()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "li-title"))
        )
        # Locate all elements with the specified class names for product names
        product_names = driver.find_elements(By.CLASS_NAME, "li-title")
        
        # Locate all elements with the specified class names for product prices
        product_prices = driver.find_elements(By.CLASS_NAME, "list_price.ineuros")
        
        # Locate all links to individual product listings
        product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/ilmoitukset/']")

        # Create an empty list to store the scraped data
        scraped_data = []

        # Iterate through the elements and extract the data
        for name_elem, price_elem, link_elem in zip(product_names, product_prices, product_links):
            product_name = name_elem.text.strip()
            product_price = price_elem.text.strip()
            product_link = link_elem.get_attribute("href")
            
            # Create a dictionary for each item
            item_data = {
                "Name": product_name,
                "Price": product_price,
                "Link": product_link
            }
            scraped_data.append(item_data)
            print(f"Scraped: {item_data}")
        # Print the list of extracted data
        for item in scraped_data:
            print(f"Product Name: {item['Name']}, Price: {item['Price']}, Link: {item['Link']}")

def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
   setUp()

