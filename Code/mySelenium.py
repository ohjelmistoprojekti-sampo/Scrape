import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class IkeaScrape(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        search_term = input("Product name: ")
        self.driver.get(f"https://www.ikea.com/fi/fi/search/?q={search_term}")

    def test_scrape_ikea(self):
        driver = self.driver
        
        # Locate all elements with the specified class names
        name_parts_1 = driver.find_elements(By.CLASS_NAME, "plp-price-module__product-name")
        name_parts_2 = driver.find_elements(By.CLASS_NAME, "plp-price-module__description")
        
        # Locate the div elements with the specified class containing price data
        price_elements = driver.find_elements(By.CSS_SELECTOR, 'div.plp-mastercard[data-price]')
        
        # Create an empty list to store the scraped data
        scraped_data = []

        # Iterate through the elements and extract the data
        for i in range(len(name_parts_1)):
            product_name = name_parts_1[i].text
            product_description = name_parts_2[i].text
            price = price_elements[i].get_attribute("data-price")
            scraped_data.append(f"Product Name: {product_name} {product_description}, Price: {price}")

        # Print the list of extracted data
        for data in scraped_data:
            print(data)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
