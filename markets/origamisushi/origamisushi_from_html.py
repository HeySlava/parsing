import json
from bs4 import BeautifulSoup
import os
import re


def get_id(sp):
    '''
    Получает строку, возвращает уникальный идентификатор
    '''

    product_string = sp.select_one('.col-12.col-sm-6 img')['src']
    product_id = re.findall('[0-9]+', product_string)[0]
    return product_id


def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    return sp.select_one('.block-detail__title').getText()


def get_group_subgroup(sp):
    '''
    Return group of product
    '''
    group_string = sp.select('.breadcrumbs a')
    group = group_string[1].getText()
    if len(group_string) == 3:
        subgroup = group_string[-1].getText()
    else:
        subgroup = None
    return group, subgroup


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    image = sp.select_one('.col-12.col-sm-6 img')['src']
    first_part = 'https://origamisushi.ru/'
    return first_part + image


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    if sp.select_one('.action-price'):
        price_string = sp.select_one('.action-price').getText()
        price_product = price_string.replace(' ₽', '')
    else:
        price_string = sp.select_one('.block-detail__price').getText()
        price_product = price_string.replace(' ₽', '')
    return price_product


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    description = sp.select_one('.block-detail__composition').getText()

    second_weight = re.search('\d+ г', description)
    if second_weight:
        end_of_description = second_weight.start()
        description = description[:end_of_description].replace('Вес:', '').strip()
        return description
    return description


def get_weight(sp):
    '''
    Return weight of product
    '''
    return sp.select_one('.block-detail-weight').getText().replace(' г.', '')


def get_additiions(sp):
    '''
    Return some topping if it is possible
    '''
    additions_dict = {}
    additions = description = sp.select_one('.block-detail__composition').getText()
    if 'Доп.:' in additions:
        # additions = additions.replace('Доп.: ', '')
        # additions = additions.split('\n')
        additions_dict['сыр/спайси'] = 15
    if additions_dict:
        return additions_dict
    return


def get_is_hot(string):
    '''
    Return True or None
    '''
    return True if 'hot' in string else None


def get_is_hit(string):
    '''
    Return True or None
    '''
    return True if 'hit' in string else None


files = os.listdir('/home/vyacheslav/parsing/origamisushi/html_pages/')

elements = []

for file in files:
    with open('/home/vyacheslav/parsing/origamisushi/html_pages/{}'.format(file)) as f:
        soup = BeautifulSoup(json.load(f), 'html.parser')

    element = {
        'id': get_id(soup),
        'group': get_group_subgroup(soup)[0],
        'subgroup': get_group_subgroup(soup)[1],
        'name': get_name(soup),
        'image': get_image(soup),
        'price': get_price(soup),
        'descr': get_description(soup),
        'weight': get_weight(soup),
        'additions': get_additiions(soup),
        'is_hot': get_is_hot(file),
        'is_hit': get_is_hit(file)
    }

    elements.append(element)

with open('/home/vyacheslav/parsing/origamisushi/origamisushi.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
