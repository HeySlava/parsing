from bs4 import BeautifulSoup
import requests
import os
import re
import time
import json


def get_id(sp):
    '''
    Получает строку, возвращает уникальный идентификатор
    '''
    return re.search('\d+', sp['id']).group()


def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    return sp.select_one('.card-title').getText()


def get_group(sp):
    '''
    Return group of product
    '''
    pass


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    return 'https://rollwell.ru' + sp.select_one('.catalog-item-photo ')['src']


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    return sp.select_one('.text-nowrap').getText().replace(' ₽', '')


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    description = sp.select_one('.card-text.small').getText()
    place_descr = re.search('Состав:', description).end()
    description = description[place_descr:].strip()
    return description


def get_weight(sp):
    '''
    Return weight of product
    '''
    weight_string = sp.select_one('.card-text.small').getText()
    weight = re.search('\d+', weight_string).group()
    return weight


def get_additiions(sp):
    '''
    Return some topping if it is possible
    '''


def get_is_hot(string):
    '''
    Return True or None
    '''


def get_is_hit(string):
    '''
    Return True or None
    '''


link = 'https://rollwell.ru/'
r = requests.get(link).text
soup = BeautifulSoup(r, 'html.parser')
chapters = soup.select('.index-sections-item a')

elements = []
for chapter in chapters:
    chapter_link = 'https://rollwell.ru' + chapter['href']
    soup = BeautifulSoup(requests.get(chapter_link).text, 'html.parser')

    group = soup.select_one('.content-header__title').getText()

    products_on_page = soup.select('.col-sm-4.col-lg-3.mb-4')
    for product_on_page in products_on_page:
        element = {
            'id': get_id(product_on_page),
            'group': group,
            'name': get_name(product_on_page),
            'image': get_image(product_on_page),
            'price': get_price(product_on_page),
            'descr': get_description(product_on_page),
            'weight': get_weight(product_on_page),
        }
        elements.append(element)
    time.sleep(2)

with open('/home/vyacheslav/parsing/rollwell/rollwell.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
