import json
import os
import pickle
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def get_data():

    if not  os.path.exists('data'):
        os.mkdir('data')
    
    try:

        options = webdriver.ChromeOptions()
        # options.add_argument("--no-sandbox")
        # options.add_argument("headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(
                executable_path=r"/usr/bin/chromedriver",
                options=options
            )

        link = 'https://www.fl.ru/projects/'
        
        driver.get(link)
        time.sleep(1)

        driver.find_element_by_css_selector('#comboe').send_keys('Программирование')
        time.sleep(0.5)
        driver.find_element_by_css_selector('#comboe').send_keys('парсинг данных')
        time.sleep(1)
        driver.find_element_by_css_selector('.b-buttons .b-button').click()

        data = []
        projects = driver.find_elements_by_css_selector('.b-post__grid')
        for project in projects:
            project_id = project.find_element_by_css_selector('a').get_attribute('name')
            project_title = project.find_element_by_css_selector('a').text
            project_href = "https://www.fl.ru" + \
                    project.find_element_by_css_selector('a').get_attribute('href')
            project_price = project.find_element_by_css_selector('.b-post__price').text
            project_descr = project.find_element_by_css_selector('.b-post__txt').text

            data.append(
                    {
                        'id': project_id,
                        'items': {
                            'title': project_title,
                            'href': project_href,
                            'description': project_descr,
                            'price': project_price
                        }
                    }
                )
            print(data)
            break


        html = driver.page_source

        html = driver.page_source
        with open('data/html.html', 'w') as file:
            file.write(html)

    finally:
        driver.quit()


if __name__ == '__main__':
    get_data()
