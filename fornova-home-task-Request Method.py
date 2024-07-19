import requests
from bs4 import BeautifulSoup
import json

def safe_extract(element, selector, attribute='text'):
    found = element.select_one(selector)
    if found:
        return getattr(found, attribute).strip() if attribute == 'text' else found[attribute]
    return None

def extract_price(element):
    price_element = element.select_one('div.css-1tu09b8-Box-Flex')
    if price_element:
        price_text = price_element.text.strip()
        try:
            return float(price_text.replace('$', '').replace(',', ''))
        except ValueError:
            return None
    return None

url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2024-08-02&checkOut=2024-08-03&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"


response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')


rates = []


rate_elements = soup.find_all('div', class_='css-8jmuus-Container e1osk7s0')

for element in rate_elements:
    rate = {
        "Room_name": safe_extract(element, 'div.css-1ca2hp6-Hide e1yh5p93'),
        "Rate_name": safe_extract(element, 'div.offer-details'),
        "Number_of_Guests": safe_extract(element, 'div.css-iux7bv-Box'),
        "Cancellation_Policy": safe_extract(element, 'div.css-1f6l7uq-Box-Flex'),
        "Price": extract_price(element,'css-1tu09b8-Box-Flex e1pfwvfi0'),
        "Is_Top_Deal": bool(element.select_one('div.css-1umloc1-Box-Flex-BadgeFrame')),
        "Currency": "AUD" 
    }
    
    
    if any(rate.values()):
        rates.append(rate)

result = {
    "rates": rates
}


result_json = json.dumps(result, indent=2)
print(result_json)


with open('rates.json', 'w') as f:
    json.dump(result, f, indent=2)