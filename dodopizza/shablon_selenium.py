from selenium import webdriver
import time
import json

driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/parsing/chromedriver")
driver.set_window_size(1500, 1000)
link = 'https://dodopizza.ru/tula'


def get_chapter(d):
    chapter_names = [x.text for x in d.find_elements_by_css_selector('.sc-814yrq-0')][:5]
    chapters = d.find_elements_by_css_selector('.sc-814yrq-2')[:5]
    chapters = zip(chapters, chapter_names)
    return chapters


def get_pizza(d, ch):
    pizzas = ch.find_elements_by_css_selector('.sc-1x0pa1d-3')
    print(len(pizzas))
    for pizza in pizzas:
        pizza.find_element_by_css_selector('.sc-1shx3k4-0 ').click()
        time.sleep(4)
        d.find_element_by_css_selector('.sc-1lk7lib-0').click()


elements = []
try:
    driver.get(link)
    time.sleep(1)
    for chapter in get_chapter(driver):
        if chapter[1] == 'Пицца':
            elements.extend(get_pizza(driver, chapter[0]))
    # # в этом блоке я получаю ссылки каждого продукта
    # menu = driver.find_element_by_css_selector('.dc-mega').click()
    # time.sleep(0.5)
    # chapters = driver.find_elements_by_css_selector('.row ul li a')
    # chapter_links = [(x.get_attribute('href'), x.text) for x in chapters]
    # for chapter_link in chapter_links:
    #     driver.get(chapter_link[0])
    #     time.sleep(1)
    #     products = driver.find_elements_by_css_selector('.border a')
    #     product_links = [x.get_attribute('href') for x in products]
    #     for product_link in product_links:
    #         c += 1
    #         driver.get(product_link)
    #         time.sleep(1)
    #         html = driver.page_source
    #         element = {
    #             'link': product_link,
    #             'group': chapter_link[1],
    #             'html': html
    #         }
    #         with open(f'/home/vyacheslav/parsing/trarottoria/html_pages/{c}.json', 'w') as f:
    #             json.dump(element, f)
finally:
    print('Done!')
    driver.quit()
