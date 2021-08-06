import re
from bs4 import BeautifulSoup
import os
import json


def get_id(sp):
    '''
    Получает строку, возвращает уникальный идентификатор
    '''

    return


def get_group(sp):
    '''
    Return group of product
    '''



def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    return


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    return


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    return


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    return


def get_weight(sp):
    '''
    Return weight of product
    '''
    return


def get_number_info(sp):
    '''
    Return total kcal and bfu
    '''
    return


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


files = os.listdir('./html_pages')
elements = []
for file in files:
    with open(f'./html_pages/{file}') as f:
        data = json.load(f)
        product_link = data['link']
        group = data['group']
        html = data['html']
        soup = BeautifulSoup(html, 'html.parser')

    element = {
        'id': get_id(soup),
        'product_link': product_link,
        'group': group,
        'name': get_name(soup),
        'image': get_image(soup),
        'price': get_price(soup),
        'descr': get_description(soup),
        'weight': get_weight(soup),
        'kcal': get_number_info(soup)
    }

with open('./trattoria.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
