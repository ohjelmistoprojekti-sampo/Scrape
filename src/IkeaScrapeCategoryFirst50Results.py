from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_ikea():
    driver = webdriver.Chrome()
    driver.get("https://www.ikea.com/fi/fi/cat/tuolit-fu002/")

    # Locate all elements with the specified class names
    name_parts_1 = driver.find_elements(By.CLASS_NAME, "pip-header-section__title--small.notranslate")
    name_parts_2 = driver.find_elements(By.CLASS_NAME, "pip-header-section__description-text")

    # Locate the div elements with the specified class containing price data
    price_elements = driver.find_elements(By.CLASS_NAME, "pip-temp-price__sr-text")

    # Create an empty list to store the scraped data
    scraped_data = []

    # Iterate through the elements and extract the data
    for i in range(len(name_parts_1)):
        product_name = name_parts_1[i].text
        product_description = name_parts_2[i].text
        price = price_elements[i].text.replace("Hinta", "").strip()


        # Create a dictionary for each item
        item_data = {"Nimi": product_name + " " + product_description,
                     "Hinta": price}
        scraped_data.append(item_data)

    # Print the list of extracted data
    for item in scraped_data:
        print(f"Product Name: {item['Nimi']}, {item['Hinta']}")
        
    print(scraped_data)

    driver.close()

if __name__ == "__main__":
    scrape_ikea()
