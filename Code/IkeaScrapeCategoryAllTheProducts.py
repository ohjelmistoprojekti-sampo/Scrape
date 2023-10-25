from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def accept_cookie_consent(driver):
    try:
        # Wait for the cookie consent button to be clickable
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        driver.execute_script("arguments[0].click();", consent_button)
    except:
        # If the button is not found or not clickable, just proceed
        pass

def scrape_ikea():
    driver = webdriver.Chrome()
    driver.get("https://www.ikea.com/fi/fi/cat/vauvojen-kalusteet-45780/")

    # Accept cookie consent
    accept_cookie_consent(driver)

    while True:
        # Scroll the page down to bring the "Näytä lisää" button into view
        driver.execute_script("window.scrollBy(0, 400)")

        # Give some time for the page to load
        time.sleep(2)

        try:
            # Locate the "Näytä lisää" button with a different locator
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Näytä lisää']"))
            )
            driver.execute_script("arguments[0].click();", show_more_button)
        except:
            # If the button is not found, break out of the loop
            break

        # Locate all elements with the specified class names
        name_parts_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-header-section__title--small.notranslate"))
        )
        name_parts_2 = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-header-section__description-text"))
        )

        # Locate the div elements with the specified class containing price data
        price_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pip-temp-price__sr-text"))
        )

        # Create an empty list to store the scraped data
        scraped_data = []

        # Iterate through the elements and extract the data
        for i in range(len(name_parts_1)):
            product_name = name_parts_1[i].text
            product_description = name_parts_2[i].text
            price = price_elements[i].text.replace("Hinta", "").strip()

            # Create a dictionary for each item
            item_data = {"Nimi": product_name + " " + product_description, "Hinta": price}
            scraped_data.append(item_data)

        # Print the list of extracted data
        for item in scraped_data:
            print(f"Product Name: {item['Nimi']}, {item['Hinta']}")

    print(scraped_data)
    print("Scraping completed.")
    driver.close()

if __name__ == "__main__":
    scrape_ikea()
