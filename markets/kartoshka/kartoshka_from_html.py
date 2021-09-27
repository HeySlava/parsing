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
    pass


def get_group(sp):
    '''
    Return group of product
    '''
    return sp.select_one('.product__headline .product__incut').getText()


def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    return sp.select_one('.product__headline .product__name').getText()


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    first_part = 'https://www.kartoshka.com'
    second_part = sp.select_one('.product__wrapper .product__img.js-lazy')['data-src']
    return first_part + second_part


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    return


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    description = sp.select_one('.product__description .product__text')
    description = str(description.getText()).strip()
    description = description.split('\n')[0]

    # if description.find('br'):
    #     description = str(description).replace('<p class="product__text">', '')
    #     end = description.find('<br/>')
    #     description = description[:end].strip()
    # else:
    #     description = description.getText().strip()
    return description


def get_weight(sp):
    '''
    Return weight of product
    '''
    weight = sp.select_one('.product__description .product__incut')
    if weight:
        return weight.getText()
    return


def get_number_info(sp, select):
    '''
    Return total kcal and bfu
    '''
    info = sp.select_one(select)
    if info:
        info = re.search('[\d]+,*[\d]*', info.getText())
        if info:
            info = info.group()
    else:
        info = None
    return info


def get_additiions(sp):
    '''
    Return some topping if it is possible
    '''
    pass


def get_is_hot(string):
    '''
    Return True or None
    '''
    pass


def get_is_hit(string):
    '''
    Return True or None
    '''
    pass


link = 'https://www.kartoshka.com/menu'
r = requests.get(link).text
soup = BeautifulSoup(r, 'html.parser')
items = soup.select('.product__item.js-product-item')

elements = []
for item in items:
    print(get_name(item))

    protein = get_number_info(item, '.product__info .product__protein')
    fats = get_number_info(item, '.product__info .product__fats')
    carbs = get_number_info(item, '.product__info .product__carbs')
    weight = get_number_info(item, '.product__description .product__incut')
    if protein and fats and carbs:
        protein, fats, carbs = (x.replace(',', '.') for x in (protein, fats, carbs))
        total_kcal = round(4 * float(protein) + 4 * float(carbs) + 9 * float(fats), 1)
        pfc = str(protein) + '/' + str(fats) + '/' + str(carbs)
    else:
        total_kcal = None
        pfc = None
    element = {
        'id': get_id(item),
        'group': get_group(item),
        'name': get_name(item),
        'image': get_image(item),
        'price': get_price(item),
        'descr': get_description(item),
        'weight': weight,
        'kcal': total_kcal,
        'p/f/c': pfc
    }

    elements.append(element)

with open('kartoshka.json', 'w', encoding='utf-8') as file:
    json.dump(elements, file, indent=4, ensure_ascii=False)

