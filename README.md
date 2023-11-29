# Scrape
This is a scraper service for `https://github.com/ohjelmistoprojekti-sampo/sampo`
## Usage
This scaper service is used in Sampo arvolaskuri project to scrape data from Tori.fi, Ikea.fi and huuto.net. Data is pushed to MongoDB database. 
### Technologies and libraries
- **Python**

- **requests**

- `https://github.com/psf/requests`

- **beautifulsoup4**

- `https://pypi.org/project/beautifulsoup4/`

- **selenium**

- `https://pypi.org/project/selenium/`

- **pymongo**

- `https://pypi.org/project/pymongo/`

- **python-dotenv**

- **chromedriver-autoinstaller**

- `https://pypi.org/project/chromedriver-autoinstaller/`

### Run webscraper
Clone the project

`git clone https://github.com/ohjelmistoprojekti-sampo/Scrape`

Install necessary dependecies with pip:

`pip install requirements.txt`
  
Run the python script
  > $ python3 src/main.py
