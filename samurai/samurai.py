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
    product_id = re.search('\d+', sp['name']).group()
    return product_id


def get_name(sp):
    '''
    Возвращает названию блюда
    '''
    name = sp.select_one('.vitrina_header a').getText()
    if re.search('\/ [0-9]+ *г', name):
        weight = re.search('\/ [0-9]+ *г', name).group()
        name = name.replace(weight, '')
    return name


def get_group(sp):
    '''
    Return group of product
    '''
    pass


def get_image(sp):
    '''
    Вовращает ссылку фотографии
    '''
    try:
        image_link = sp.select_one('a')['href']
    except Exception:
        print('No big photo')
        image_link = 'http://samurai-tula.ru' + sp.select_one('img')['src']
    return image_link


def get_price(sp, sp_name):
    '''
    Возвращает цену продуктра
    '''
    name = sp_name.select_one('.vitrina_header a').getText()
    if 'Пицца' in name:
        pizza_dict = {}
        price_string1 = sp.select_one('.line_1').getText()
        if price_string1:
            size1 = re.search('\d+ *см', price_string1)
            if size1:
                size1 = size1.group()
            price1 = re.search('((\d+) *руб)', price_string1)
            if price1:
                price1 = price1.groups()[1]
            pizza_dict['var1'] = size1
            pizza_dict['price1'] = price1
            # print(size1, price1)

        price_string2 = sp.select_one('.line_2')
        if price_string2:
            price_string2 = price_string2.getText()
            size2 = re.search('\d+ *см', price_string2)
            if size2:
                size2 = size2.group()
            price2 = re.search('((\d+) *руб)', price_string2)
            if price2:
                price2 = price2.groups()[1]
            pizza_dict['var2'] = size2
            pizza_dict['price2'] = price2
            # print(size2, price2)
        return pizza_dict
    else:
        price_string = sp.select_one('.line_1').getText()
        price = re.search('\d+', price_string).group()
        return {'price': price}


def get_description(sp):
    '''
    Возвращает описание продукта
    '''
    description_string = sp.select_one('.shopwindow_content')
    if description_string:
        description_string = description_string.getText()
        return description_string
    return


def get_weight(sp):
    '''
    Return weight of product
    '''
    weight = sp.select_one('.vitrina_header a').getText()
    if re.search('\/ [0-9]+ *г', weight):
        weight = re.search('(\/ ([0-9]+) *г)', weight).groups()[1]
        return weight
    return


def get_additiions(sp):
    '''
    Return some topping if it is possible
    '''


def get_is_vega(string):
    '''
    Return True or None
    '''
    return 'vega.' in str(string['src'])


def get_is_hot(string):
    '''
    Return True or None
    '''
    return 'hot.' in str(string['src'])


def get_is_hit(string):
    '''
    Return True or None
    '''
    return 'hit.' in str(string['src'])


def get_is_new(string):
    '''
    Return True or None
    '''
    return 'new.' in str(string['src'])


link = 'http://samurai-tula.ru/samurai-menu/'
r = requests.get(link).text
soup = BeautifulSoup(r, 'html.parser')
sections = soup.select('.tile a')

elements = []
for section in sections:
    chapter_link = 'http://samurai-tula.ru' + section['href']
    soup = BeautifulSoup(requests.get(chapter_link).text, 'html.parser')
    time.sleep(1)

    group_name = soup.select_one('.post-title').getText()
    page_number = 2 if soup.select('.wpshop_pagg a') else 1
    # if soup.select('.wpshop_pagg a'):
    #     page_number = 2
    # else:
    #     page_number = 1
    for i in range(1, page_number+1):
        several_pages_link = chapter_link + f'/?vpage={i}'
        soup = BeautifulSoup(requests.get(several_pages_link).text, 'html.parser')

        icons = soup.select('.label1')
        vetrina_elements = soup.select('.vitrina_element')
        wpshop_bags = soup.select('.wpshop_bag input')
        price_block = soup.select('.wpshop_buy')
        products_on_page = zip(icons, vetrina_elements, wpshop_bags, price_block)
        for product_on_page in products_on_page:
            print(get_name(product_on_page[1]))
            element = {
                'id': get_id(product_on_page[2]),
                'group': group_name,
                'name': get_name(product_on_page[1]),
                'image': get_image(product_on_page[1]),
                # 'price': get_price(product_on_page[3], product_on_page[1]),
                'descr': get_description(product_on_page[1]),
                'weight': get_weight(product_on_page[1]),
                'is_new': get_is_new(product_on_page[0]),
                'is_vega': get_is_vega(product_on_page[0]),
                'is_hot': get_is_hot(product_on_page[0]),
                'is_hit': get_is_hit(product_on_page[0]),
            }
            element.update(get_price(product_on_page[3], product_on_page[1]))
            elements.append(element)
        time.sleep(0.5)

with open('/home/vyacheslav/parsing/samurai/samurai.json', 'w', encoding='utf-8') as fs:
    json.dump(elements, fs)
