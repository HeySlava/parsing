from selenium import webdriver
import time
import json

driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/parsing/chromedriver")

driver.set_window_size(1500, 1000)

link = 'https://origamisushi.ru/'

driver.get(link)

product_links = []
chapter_links = []

try:
    time.sleep(1)

    # в этом блоке я получаю ссылки каждого продукта
    chapters = driver.find_elements_by_css_selector('.col-md-3.col-6')

    for chapter in chapters:
        chapter_link = chapter.find_element_by_css_selector('a').get_attribute('href')
        chapter_links.append(chapter_link)

    for chapter_link in chapter_links:
        driver.get(chapter_link)
        time.sleep(1)

        products = driver.find_elements_by_css_selector('.item-shop')

        for product in products:
            icons = product.find_elements_by_css_selector('.item-icon img')
            string = ''
            if len(icons) > 0:
                for icon in icons:
                    string += icon.get_attribute('src')

            if 'hot.png' in string:
                is_hot = True
            else:
                is_hot = False

            if 'hit.png' in string:
                is_hit = True
            else:
                is_hit = False

            product_link = product.find_element_by_css_selector('a').get_attribute('href')
            product_links.append((product_link, is_hot, is_hit))
        driver.back()
        time.sleep(1)

    #     В этом блоке я прохожусь по ссылкам и сохраняю страницы
    c = 0
    for product_link in product_links:
        c += 1
        driver.get(product_link[0])
        time.sleep(1)

        html_page = driver.page_source
        name = str(c) + '_hot'*product_link[1] + '_hit'*product_link[2]
        print(name)

        with open('/home/vyacheslav/parsing/origamisushi/html_pages/{}.txt'.format(name), 'w') as sf:
            json.dump(html_page, sf)

finally:
    print('Done!')
    driver.quit()
