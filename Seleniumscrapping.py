from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
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
    driver.maximize_window()
    driver.get("https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-08-02&checkOut=2024-08-03&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity")
    time.sleep(20)
    data=[]
    try:
        for e in driver.find_elements(By.XPATH,'//div[contains(@class, "css-du5wmh-Box")]'):
            room_name=e.find_element(By.XPATH,'.//*[contains(@class, "css-19vc6se-Heading-Heading-Text")]').text
            for i in e.find_elements(By.XPATH,'.//*[contains(@class, "css-1wzt5tj-Box")]'):
                try:
                    rate_name = i.find_element(By.XPATH,'.//h3[contains(@class, "css-6qo8xy-Heading-Heading-Text")]').text
                except:
                    rate_name = i.find_element(By.XPATH,'.//h3[contains(@class, "css-10yvquw-Heading-Heading-Text")]').text
                cancel =  i.find_element(By.XPATH, './/*[@id="cancellation-policy-button"]').text
                facilities =  i.find_element(By.XPATH, './/*[contains(@class, "css-rz7hex-Text")]').text
                price =  i.find_element(By.XPATH, './/span[contains(@data-testid, "amount")]').text
                deal = True if i.find_element(By.XPATH, './/span[contains(@class, "css-1jr3e3z-Text-BadgeText")]').text == "TOP DEAL" else False
                try:
                    guest = i.find_element(By.XPATH,'.//span[contains(@data-testid, "guests")]').text
                except Exception as e:
                    guest = i.find_element(By.XPATH,'.//span[contains(@data-testid, "offer-guest-text")]').text.replace("1 night from", "")
                d={
                    "Room_name": room_name,
                    "Rate_name": rate_name,
                    "Number_of_Guests": guest,
                    "Cancellation_Policy": cancel,
                    "Facilities": facilities,
                    "Price": price,
                    "Is_Top_Deal": deal,
                    "Currency": "AUD"
                }
                data.append(d)
    except Exception as e:
        print("something went wrong")
    driver.quit()
    return data

result=run()
result_json = json.dumps(result, indent=2)
print(result_json)


with open('rates.json', 'w') as f:
    json.dump(result, f, indent=2)
 
