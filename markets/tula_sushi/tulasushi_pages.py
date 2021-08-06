import re
from selenium import webdriver
import time
import json

driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/parsing/chromedriver")
driver.set_window_size(1500, 1000)
link = 'https://tula-sushi.ru/'
c = 0
try:
    driver.get(link)
    time.sleep(1)
    # get link of each product
    chapters = driver.find_elements_by_css_selector('.catalog-main a')
    # link, title of each chapter
    chapter_info = [(x.get_attribute('href'), x.get_attribute('title')) for x in chapters]
    for chapter in chapter_info:
        driver.get(chapter[0])
        time.sleep(1)
        products = driver.find_elements_by_css_selector('.mini-card-wrap')
        # href, name_chapter, id, is_new, is_action
        product_links = [(x.find_element_by_css_selector('.mini-card-img a').get_attribute('href'),
                          x.find_element_by_css_selector('.mini-card-img a').get_attribute('title'),
                          x.find_element_by_css_selector('div').get_attribute('id'),
                          x.find_elements_by_css_selector('.flags.color17'),
                          x.find_elements_by_css_selector('.flags.color18')) for x in products]

        for product_info in product_links:
            time.sleep(1)
            if product_info[3]:
                is_new = 1
            else:
                is_new = 0
            if product_info[4]:
                is_action = 1
            else:
                is_action = 0

            driver.get(product_info[0])
            time.sleep(1)
            html = driver.page_source
            element = {
                'link': product_info[0],
                'group': chapter[1],
                'is_action': is_action,
                'is_new': is_new,
                'html': html
            }
            print(element)
            print(product_info[2])
            print()
            with open(f'/home/vyacheslav/parsing/tula_sushi/html_pages/{product_info[2]}.json', 'w') as f:
                json.dump(element, f)
finally:
    print('Done!')
    driver.quit()
