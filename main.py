from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import datetime

driver = webdriver.Chrome("C:\\SeleniumDrivers\\chromedriver.exe")
url = "https://getgems.io/"
driver.get(url=url)

time.sleep(1)

# SCROLL THE PAGE
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# FINDING ALL COLLECTIONS AT PAGE
elements = driver.find_elements(By.CLASS_NAME, "CollectionPreview")

# CREATE DICTIONARY FROM ALL FINDED COLLECTIONS WITH LINKS
collections = {}
for element in elements:
    collection_title = element.find_element(By.CLASS_NAME, "CollectionPreview__title").get_attribute('title')
    collection_link = element.get_attribute('href')
    collections[collection_title] = collection_link

# PARSE ALL LINKS AND GETTING COLLECTIONS DATA
for collection in collections:  
    driver.get(collections[collection])
    collection_all_info = driver.find_elements(By.CLASS_NAME, "EntityPageStatistics__item-inner")
    collection_info = { "DESCRIPTION": driver.find_element(By.CLASS_NAME, "EntityPageDescription").text,
                        "LINK": collections[collection]
                        }
    collection_data = {}
    for col in collection_all_info:
        key = col.find_element(By.CLASS_NAME, "EntityPageStatistics__key")
        value = col.find_element(By.CLASS_NAME, "EntityPageStatistics__value")
        collection_data[key.text] = value.text
    collection_info['DATA'] = collection_data
    collections[collection] = collection_info

# SAVE ALL DATA IN JSON FILE
with open("getgems_collections_"+ str(datetime.date.today()) +".json", "w", encoding="UTF-8") as file:
    json.dump(collections, file, indent=4, ensure_ascii=False)