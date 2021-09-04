import json
import os
import pickle
import time
import datetime
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

        current_time = int(time.time())
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
                            'price': project_price,
                            'time': f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}'
                            
                        }
                    }
                )

    finally:
        driver.quit()
        return data


def update_posts(dict):

    if not os.path.isfile('data/posts.json'):
        with open('data/posts.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    else:
        with open('data/posts.json') as file:
            local_dict = json.load(file)

        new_dict = []
        for item in dict:
            if item not in local_dict:
                new_dict.append(item)

        local_dict.extend(dict)
        with open('data/posts.json', 'w') as file:
            json.dump(local_dict, file, indent=4, ensure_ascii=False)
    
        print(new_dict)


if __name__ == '__main__':
    update_posts(get_data())

