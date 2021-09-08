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

    headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Is-Ajax-Request": "X-Is-Ajax-Request",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
    
    try:

        options = webdriver.ChromeOptions()
        # options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')
        options.add_argument("--no-sandbox")
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

        current_time = int(time.time())
        data = []
        projects = driver.find_elements_by_css_selector('.b-post__grid')
        for project in projects:
            project_id = project.find_element_by_css_selector('a').get_attribute('name')
            project_title = project.find_element_by_css_selector('a').text
            project_href =  \
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
                            'time': f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}',
                            'unix': int(time.time())
                            
                        }
                    }
                )

        return data

    finally:
        driver.quit()


def update_posts(dict_posts):

    if not os.path.exists('data/posts.json'):
        with open('data/posts.json', 'w') as file:
            json.dump(dict_posts, file, indent=4, ensure_ascii=False)

    else:

        with open('data/posts.json') as file:
            local_dict = json.load(file)

        old_orders_id = [i['id'] for i in local_dict]
        news = []
        for item in dict_posts:
            if item['id'] not in old_orders_id:
                news.append(item)

        with open('data/posts.json', 'w') as file:
            json.dump([*news, *local_dict], file, indent=4, ensure_ascii=False)

        return news


if __name__ == '__main__':
    update_posts(get_data())

