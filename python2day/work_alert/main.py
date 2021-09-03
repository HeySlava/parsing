from datetime import datetime
from selenium import webdriver
import os
import pickle
import time
import json


def get_data():
    
    try:

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(
                executable_path=r"/usr/bin/chromedriver",
                options=options
            )

        link = 'https://www.fl.ru/'
        
        # driver.get(link)
        # time.sleep(1)
        # test = driver.select('h2.b-page__title')
        # print(test)

        html = driver.page_source

        with open('index.html', 'w') as file:
            json.dump(html, file, indent=4, ensure_ascii=False)

    finally:
        driver.quit()


if __name__ == '__main__':
    get_data()
