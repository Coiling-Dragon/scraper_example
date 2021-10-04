"""
@author: CoilingDragon

# https://chromedriver.chromium.org/downloads
# my chrome driver version is 94


beautifulsoup4==4.9.0
selenium==3.141.0
"""

from bs4 import BeautifulSoup
import time
import json
import re


from selenium                                import webdriver
from selenium.webdriver.common.by            import By
from selenium.webdriver.support.ui           import WebDriverWait
from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.chrome.options       import Options


def wait_for_ready(selector):
    '''
        As this function returns result or False, 
        it can be used to check for existance of selectors
    '''
    try:
        ready = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , selector)))
        return ready
    except:
        print(f'Timeout {selector}')   
        return False


url = 'https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
driver.implicitly_wait(1)
driver.get(url)

#One sec sleep to make sure driver is booted
time.sleep(1)


name_selector = '.product-name'
price_selector = '.product-sale'
color_selector = '.colors-info-name'

product_name = wait_for_ready(name_selector)
product_price = wait_for_ready(price_selector)
product_color = wait_for_ready(color_selector)


dr_response = wait_for_ready('.product-actions')
dr_response = dr_response.get_attribute('innerHTML')
soup = BeautifulSoup(dr_response, 'html.parser')
selector_list = soup.find("div",class_='selector-list')
sizes = [item['data-size'] for item in selector_list.find_all('span', attrs={'data-size' : True})]

#regex to clean the price
product_price = re.findall(r'[0-9]+.[0-9]+',product_price.text)[0]

json_dict = {
  "name": product_name.text,
  "price": float(product_price),
  "color": product_color.text,
  "size": sizes
}

json_string = json.dumps(json_dict)

print(json_string)
with open('data.json','w') as file:
    file.write(json_string)


driver.close()