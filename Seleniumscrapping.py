from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

# configure Chrome Webdriver
def configure_chrome_driver(headless=False):
    # Add additional Options to the webdriver
    chrome_options = ChromeOptions()
    
    # add the argument and make the browser Headless.
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # To bypass chrome headless being detected  by urls issue      
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        # log-level:
        # Sets the minimum log level.
        # Valid values are from 0 to 3:
 
        #     INFO = 0,
        #     WARNING = 1,
        #     LOG_ERROR = 2,
        #     LOG_FATAL = 3.
 
        # default is 0
        chrome_options.add_argument('log-level=3')
    # Download chrome driver in cache
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver
def run():
    driver=configure_chrome_driver()
    g=driver.get("https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-08-02&checkOut=2024-08-03&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity")
    time.sleep(20)
    # html=driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    data=[]
   
    for e in driver.find_elements(By.XPATH,'//*[contains(@class, "css-3c0j8b-Box-Flex")]'):

      
        room_name=e.find_element(By.XPATH,'//*[contains(@class, "css-19vc6se-Heading-Heading-Text")]')
        import pdb; pdb.set_trace()
        for i in driver.find_elements(By.CLASS_NAME,'css-1wzt5tj-Box e1m6xhuh0'):
            d={
                "Room_name": room_name,
                "Rate_name": i.find_element(By.XPATH,'//h3')
        # "Number_of_Guests": safe_extract(element, 'div.css-iux7bv-Box'),
        # "Cancellation_Policy": safe_extract(element, 'div.css-1f6l7uq-Box-Flex'),
        # "Price": extract_price(element),
        # "Is_Top_Deal": bool(element.select_one('div.css-1umloc1-Box-Flex-BadgeFrame')),
        # "Currency": "USD"  # Assuming USD, adjust if needed
            }
            data.append(d)
    
    return g

run()