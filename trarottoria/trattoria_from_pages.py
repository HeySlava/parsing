import re

from bs4 import BeautifulSoup
import os
import json


def get_id(sp):
    '''
    Получает строку, возвращает уникальный идентификатор
    '''

    product_id = sp.select_one('.box img')
    if product_id:
        product_id = product_id['id'].replace('dp', '')
    return product_id


def get_group(sp):
    '''
    Return group of product
    '''



def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    name = sp.select_one('.wrapper h1')
    weight = None
    if name:
        name = name.getText()
        ml = re.search('((\d+)\s*мл+\.*)', name)
        ml_weight = str(ml.group(2)) if ml else ''
        ml = ml.group(1) if ml else ''

        gr = re.search('((\d{2,})\s*г+р*\.*)', name)
        gr_weight = str(gr.group(2)) if gr else ''
        gr = gr.group(1) if gr else ''

        kcal = re.search('((\d+)\s*ккал\.*)', name)
        kcal = kcal.group(1) if kcal else ''

        name = name.replace(ml, '').replace(gr, '').replace(kcal, '').replace('(', '').replace(')', '')
        name = name.strip().strip(',').strip()
        weight = ml_weight + gr_weight
    if not weight:
        weight = None
    return name, weight


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    image = sp.select_one('.box img')
    if image:
        image = 'http://trattoria-tula.ru' + image['src']
    return image


def get_price(sp):
    '''
    Возвращает цену продуктра
    '''
    price = sp.select_one('.top h1 i')
    if price:
        price = price.getText()
        price = re.search('[\d]+', price).group()
    return price



def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    description = sp.select_one('.fontstyle0, .top div')
    if description:
        description = description.get_text()

        ml = re.search('\d+\s*мл+\.*', description)
        ml = ml.group() if ml else ''

        gr = re.search('\d{2,}\s*г+р*\.*', description)
        gr = gr.group() if gr else ''

        kcal = re.search('\d+\s*ккал\.*', description)
        kcal = kcal.group() if kcal else ''

        description = description.replace(ml, '').replace(gr, '').replace(kcal, '').replace('(', '').replace(')', '').replace('\n', '')
        description = description.strip().strip(',').strip()
    if description == '':
        return None
    else:
        return description


def get_weight(sp):
    '''
    Return weight of product
    '''
    weight = sp.find(re.compile('[^h1]+[^title]+'), string=re.compile('([\d]+\s*г+)|([\d]+\s*мл+)'))
    if weight:
        answer = re.findall('[\d]+\s*г+', weight.get_text()) + re.findall('[\d]+\s*мл+', weight.get_text())
        answer = [re.search('\d+', x).group() for x in answer]
        return answer[0]
    return


def get_number_info(sp):
    '''
    Return total kcal and bfu
    '''
    kcal = sp.select_one('.fontstyle0, .top div')
    if kcal:
        kcal = kcal.get_text()
        kcal = re.search('((\d+)\s*ккал\.*)', kcal)
        kcal = kcal.group(2) if kcal else ''
    if kcal == '':
        return None
    else:
        return kcal

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
        'name': get_name(soup)[0],
        'image': get_image(soup),
        'price': get_price(soup),
        'descr': get_description(soup),
        'weight': get_weight(soup),
        'kcal': get_number_info(soup)
    }
    if not element['weight']:
        element['weight'] = get_name(soup)[1]
    elements.append(element)


with open('./trattoria.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
