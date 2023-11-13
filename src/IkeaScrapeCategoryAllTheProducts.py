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

        # Locate all the elements under the specified class containing the image link
        image_elements = driver.find_elements(By.CSS_SELECTOR, ".pip-product-compact__main-box--main .pip-image")

        # Create an empty list to store the scraped data
        scraped_data = []

         # Iterate through the elements and extract the data
        for item in product_items:
            product_name = item.find_element(By.CLASS_NAME, "pip-header-section__title--small.notranslate").text
            product_description = item.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
            price_str = item.find_element(By.CLASS_NAME, "pip-temp-price__sr-text").text.replace("Hinta", "").strip()
        
             # Convert "Hinta" to an integer
            price = int(price_str.replace(' ', ''))  # Assuming the price contains spaces

            # Extract the first image source (URL) for the current product
            image_element = item.find_element(By.CSS_SELECTOR, ".pip-product-compact__main-box--main .pip-image")
            image_src = image_element.get_attribute("src")

            # Convert "Kunto" to an integer (assuming it's a numerical value)
            kunto = 5  # Replace with the actual value if available as an integer

            # Create a dictionary for each item
            item_data = {"Nimi": product_name + " " + product_description,
                        "Hinta": price,
                        "Kunto": kunto,
                        "Kuva": image_src}
            scraped_data.append(item_data)

        # Print the list of extracted data
        for item in scraped_data:
            print(f"Product Name: {item['Nimi']}, {item['Hinta']}, {item['Kuva']}")
    driver.close()
    print(scraped_data)
    
    print("Scraping completed.")
    return(scraped_data)

if __name__ == "__main__":
    scrape_ikea()
    
