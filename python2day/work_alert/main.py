import json
import os
import pickle
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def get_list():

    try:

        options = webdriver.ChromeOptions()
        # options.add_argument("--no-sandbox")
        options.add_argument("headless")
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
        time.sleep(1)
        projects = driver.find_elements_by_css_selector('.b-post__grid')
        projects_id = [project.find_element_by_css_selector('a').get_attribute('id') for project in projects]
        return zip((projects_id, projects))

    finally:
        driver.quit()


def save_data(project):

    try:

        project_id = project.find_element_by_css_selector('a').get_attribute('name')
        project_title = project.find_element_by_css_selector('a').text
        project_href = "https://www.fl.ru" + \
                project.find_element_by_css_selector('a').get_attribute('href')
        project_price = project.find_element_by_css_selector('.b-post__price').text
        project_descr = project.find_element_by_css_selector('.b-post__txt').text

        data = {
                'id': project_id,
                'items': {
                    'title': project_title,
                    'href': project_href,
                    'description': project_descr,
                    'price': project_price,
                    'time': f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}'

                    }
            }
    finally:

        with open('data/posts.json', 'a', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def get_update():

    with open('data/posts.json', encoding='utf-8') as file:
        projects = json.load(file)

    for i in projects:
        print(i['id'])


if __name__ == '__main__':
    get_update()
