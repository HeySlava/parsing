import re
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

link = 'https://sushiwok.ru/tula/'
driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/.config/JetBrains/PyCharm2020.3/scratches/chromedriver")
driver.set_window_size(1500, 768)
driver.get(link)

wok_tula = {'wok_tula': {
    'section': {

    }}}
time.sleep(2)
try:
    # принимаю куки
    driver.find_element_by_css_selector('.sw-button').click()
    # выбираю кнопку меню и нажимаю на нее
    driver.find_element_by_css_selector('[href="/tula/menu/"]').click()
    time.sleep(1)

    # нахожу раздели и сохраняю их
    chapters = driver.find_elements_by_css_selector('.menu-item')
    links = []
    #  нахожу разделы и пробегаюсь по каждому
    for chapter in chapters:
        links.append(chapter.get_attribute('href'))

    for link in links:
        driver.get(link)
        time.sleep(2)
        # прохожусь по меню в каждом разделе
        page_title = driver.find_element_by_css_selector('.page-title').text
        elements = driver.find_elements_by_css_selector('[itemscope].card-wrapper--grid')

        wok_tula['wok_tula']['section'][page_title] = {}
        for el in elements:
            data_id = el.find_element_by_css_selector('a').get_attribute('data-id')
            name = el.find_element_by_css_selector('.card__name').text

            photo_link = el.find_element_by_css_selector('img').get_attribute('src')
            # photo_link = photo_link.replace('blob:', '')
            # проверка на наличие акции
            try:
                if el.find_element_by_css_selector('.card__is-action'):
                    is_action = True
            except:
                is_action = False

            # проверка на NEW
            is_new = el.find_element_by_css_selector('.card__newbox--new').text.strip()
            if is_new == '':
                is_new = False
            else:
                is_new = True
            # проверка на перчик
            try:
                if el.find_element_by_css_selector('.card__hot-icon'):
                    is_hot = True
            except:
                    is_hot = False
            # проверка на веганство
            try:
                if el.find_element_by_css_selector('.card__vegan-icon'):
                    is_vegan = True
            except:
                    is_vegan = False
            # доставю список ингридиентов
            ingredients = el.find_element_by_css_selector('.card__ingredients').text
            # вытаскиваю вес
            weight = el.find_element_by_css_selector('.card__ingredients span').text
            # удаляю вес из ингридиентов
            if weight in ingredients:
                ingredients = ingredients.replace(weight, '')

            price = el.find_element_by_css_selector('.card__price__and__buybutton span:nth-child(2)').text

            # проверка на наличие топингов, если есть, собрать все данные оттуда
            try:
                if el.find_element_by_css_selector('.card-topping-tag span'):
                    el.find_element_by_css_selector('.card-topping-tag span').click()
                    time.sleep(1)
                    toppings = {}
                    topps = driver.find_elements_by_css_selector('.modal-toppings__item')
                    for topping in topps:
                        topping_name = topping.find_element_by_css_selector('.modal-toppings__name').text
                        topping_price = topping.find_element_by_css_selector('.modal-toppings__price').text
                        toppings[topping_name] = topping_price
                    # print(toppings)
                    # закрываю вкладку топингов
                    driver.find_element_by_css_selector('.close-modal-btn').click()
                    time.sleep(2)

            except:
                toppings = None

            #     собираю все данные в один большой словарь
            wok_tula['wok_tula']['section'][page_title][name] = {'data_id': data_id,
                                                                 'photo_link': photo_link,
                                                                 'is_new': is_new,
                                                                 'is_action': is_action,
                                                                 'is_hot': is_hot,
                                                                 'is_vegan': is_vegan,
                                                                 'ingredients': ingredients,
                                                                 'is_toppings': toppings,
                                                                 'weight': weight,
                                                                 'price': price}
        driver.back()
        time.sleep(5)

# этот раздел выполняется в любом случае, даже если в программе была ошибка
finally:
    # time.sleep(30)
    # сохраняю словарь как json file
    with open('/home/vyacheslav/parsing/wok/wok_tula.json', 'w', encoding='utf-8') as fp:
        json.dump(wok_tula, fp)
    #     закрываю браузер
    driver.quit()
    print('Done')
