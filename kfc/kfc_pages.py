from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/parsing/chromedriver")

driver.set_window_size(1500, 1000)

link = 'https://www.kfc.ru/'

driver.get(link)

product_links = []
try:
    time.sleep(1)
    driver.find_element_by_xpath("//*[contains(text(), 'Выбрать другой')]").click()
    button = driver.find_element_by_css_selector('._3imKbwUNVp')
    button.send_keys('Тула')
    time.sleep(0.5)
    tula = driver.find_elements_by_xpath("//*[contains(text(), 'Тула')]")
    tula[-1].click()

    time.sleep(1)

    # согласился на куки
    driver.find_element_by_css_selector('._3e1-bSR94Y').click()
    # нашел разделы
    chapters = driver.find_elements_by_css_selector('._2kPVuJ4Km5')[1:]

    for chapter in chapters:
        group = chapter.find_element_by_css_selector('.t-xl span').text
        selenium_products = chapter.find_elements_by_css_selector('._1COQ_4eAC6')

        for selenium_product in selenium_products:
            link = selenium_product.find_element_by_css_selector('a').get_attribute('href')
            # print(group, link)
            product_links.append((group, link))

    for group_link in product_links:
        item_id = group_link[1].split('product/')[-1]
        driver.get(group_link[1])
        time.sleep(2)

        product = {}
        html_description = driver.page_source
        product['group'] = group_link[0]
        product['html_description'] = html_description

        with open('/home/vyacheslav/parsing/kfc/html_garbage/description_{}.json'.format(item_id), 'w') as df:
            print(group_link[1], item_id)
            json.dump(product, df)

        try:
            driver.find_element_by_css_selector('.uHW_pbqt2f').click()
        finally:
            pass
        time.sleep(0.5)

        try:
            driver.find_element_by_css_selector('._2Z1QVx9dQt').click()
        except:
            pass
        time.sleep(0.5)

        product = {}
        html_structure = driver.page_source
        product['group'] = group_link[0]
        product['html_structure'] = html_structure

        with open('/home/vyacheslav/parsing/kfc/html_garbage/structure_{}.json'.format(item_id), 'w') as sf:
            print(group_link[1], item_id)
            json.dump(product, sf)

finally:
    driver.quit()
    print('Мне кажется что это задача уже выполнена')
    pass
