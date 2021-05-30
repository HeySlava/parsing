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
    return sp.select_one('.h1-title').text


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    image = sp.select_one('.product-img img')['src']
    return image


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    price = sp.select_one('.price-full-card-value .field-item.even').text
    return price


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    try:
        description = sp.select_one('.prop-value p').text
    except Exception:
        print('There are not description')
        description = None
    return description


def get_weight(sp):
    '''
    Return weight of product
    '''
    weight_dict = {}
    pizza = re.compile('\d+\sсм')
    pieces = re.compile('\d+\sштук')
    try:
        weight = sp.select_one('.field-name-field-ves .field-item.even').text

        if pizza.search(weight):
            weight_dict['size'] = pizza.search(weight).group()
            weight_dict['weight'] = re.search('((\d+)\sграмм)', weight).group(2)
        elif pieces.search(weight):
            weight_dict['size'] = pieces.search(weight).group()
            weight_dict['weight'] = re.search('((\d+)\sграмм)', weight).group(2)
        else:
            weight_dict['weight'] = re.search('\d+[.,]*\d+', weight).group()
        return weight_dict
    except Exception:
        print('There are not value')
        return weight_dict


def get_float(string):
    return re.search('\d+[.,]*\d*', string).group().replace(',', '.')


def get_number_info(sp):
    '''
    Return total kcal and bfu
    '''

    fats = sp.select_one('.field-name-field-gur .even')
    proteins = sp.select_one('.field-name-field-bel .even')
    carbohydrates = sp.select_one('.field-name-field-ygl .even')
    if fats and proteins and carbohydrates:
        fats, proteins, carbohydrates = map(get_float, (x.text for x in [fats, proteins, carbohydrates]))
        kcal = round(4 * (float(proteins) + float(carbohydrates)) + 9 * float(fats), 1)
        pfc = '/'.join([proteins, fats, carbohydrates])
        return pfc, kcal
    else:
        return None, None
        

def get_additiions(sp):
    '''
    Return some topping if it is possible
    '''


def get_is_hot(string):
    '''
    Return True or None
    '''
   
   
def get_is_new(sp):
    """
    Return True or None
    """    
    try:
        flag = sp.select_one('.flags')
        print(flag)
    except ValueError:
        print('Bad flag')


def get_is_hit(string):
    '''
    Return True or None
    '''


files = os.listdir('./html_pages')
elements = []
problem_files = []
count = 0
for file in files:
    with open(f'./html_pages/{file}') as f:
        try:
            data = json.load(f)
            print(data)
            product_link = data['link']
            group = data['group']
            html = data['html']
            is_action = bool(data['is_action'])
            is_new = bool(data['is_new'])
            soup = BeautifulSoup(html, 'html.parser')
            print(product_link)
        except Exception:
            print(f'There is not such file -> {file}')
            count += 1
            problem_files.append(file)


    element = {
        'id': re.search('\d+', file).group(),
        'product_link': product_link,
        'group': group,
        'name': get_name(soup),
        'image': get_image(soup),
        'price': get_price(soup),
        'is_action': is_action,
        'is_new': is_new,
        'descr': get_description(soup),
        # 'weight': get_weight(soup),
        'pfc': get_number_info(soup)[0],
        'kcal': get_number_info(soup)[1]
    }
    element.update(get_weight(soup))
    elements.append(element)
    print()

with open('./tulasushi.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
