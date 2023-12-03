# Scrape
This is a scraper service for `https://github.com/ohjelmistoprojekti-sampo/sampo`
## Usage
This scaper service is used in Sampo arvolaskuri project to scrape data from Tori.fi, Ikea.fi and huuto.net. Data is pushed to MongoDB database. 
## Good to know
There is some good practises related to scraping. It is advisable to review the page's robots.txt and terms of use in case scraping is prohibited on that particular page. The collected data should not be protected by copyright law or contain personal information. Private information should also not be disseminated publicly. The website should not be overloaded to avoid blocking access to it. In the worst case, improper scraping may lead to legal actions, but retrieving public information for personal use, such as a school project, is unlikely to cause problems.
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

Install necessary dependecies with pip (With Python3 use pip3):

`pip install requirements.txt`
  
Run the python script
  > $ python3 src/main.py
