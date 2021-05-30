import json
from bs4 import BeautifulSoup
import os
import re


def get_id(string):
    return re.findall('[0-9]+', string)[0]


def get_name(sp):
    return sp.select_one('.h1').getText()


def get_comment(sp):
    try:
        comment = sp.select_one('.t-xl.c-description').getText()
    except:
        try:
            comment = sp.select_one('.button-primary.mb-32').getText()
        except:
            comment = None

    return comment


def get_image(sp):
    image_container = sp.select_one('._3JZhcrRlSI .u8CYTZzjqL')['style']
    image_ref = re.findall('\(.*?\)', image_container)[-1][1:-1]
    return image_ref


def description(sp):
    try:
        desc = sp.select_one('.t-sm.mb-32').getText()
    except:
        desc = None
    return desc


def consistency(sp):
    try:
        consis = sp.select_one('.t-sm.mb-16').getText()
        return consis.replace('Состав: ', '')
    except:
        return None


def calories(sp):
    try:
        return sp.select_one('.t-md.condensed .mr-24').getText()
    except:
        return None


def proteins(sp):
    try:
        prot = sp.select('.t-md.condensed .mr-24')

        p = prot[1].getText().replace(' г', '')
        f = prot[2].getText().replace(' г', '')
        c = prot[3].getText().replace(' г', '')
        return '{}/{}/{}'.format(p, f, c)
    except:
        return None


def toppings(sp):
    topps = {}
    try:
        topps_select = sp.select('._34QV-WxTwk')
        for top in topps_select:
            add = top.select_one('._1I_QNe9fUD').getText()
            add_name = ' '.join([x for x in re.findall('[а-яА-Я]+', add)])
            add_price = re.findall('[0-9]+', add)[-1]
            topps[add_name] = add_price
        if not topps:
            return None
        return topps
    except:
        return None


def product_price(sp):
    return sp.select_one('._1_pmQWiEB3').getText().replace('₽', '')


def product_weight(sp):
    try:
        return sp.select_one('.t-xl.mb-16.condensed').getText()
    except:
        return None


def vars_product(sp):
    vars_dict = {}
    try:
        find_vars = sp.select('.S574ENRim5')
        var_count = len(find_vars)

        for var in find_vars:
            var_name = var.select_one('.d5AWslH2hX').getText()
            var_price = var.select_one('._2mc6ha4NEP').getText().replace('₽ ', '')
            vars_dict[var_name] = var_price
        return var_count, vars_dict
    except:
        return None


files = os.listdir('/home/vyacheslav/parsing/kfc/html_garbage/')

description_list = []
structure_list = []

for file in files:
    if 'description' in file:
        description_list.append(file)
    elif 'structure' in file:
        structure_list.append(file)

structure_list.sort(key=lambda x: re.findall('[0-9]+', x)[-1])
description_list.sort(key=lambda x: re.findall('[0-9]+', x)[-1])

elements = []

two_html = zip(description_list, structure_list)
for html_tuple in two_html:
    descr_page = html_tuple[0]
    struct_page = html_tuple[1]

    with open('/home/vyacheslav/parsing/kfc/html_garbage/{}'.format(descr_page)) as json_file:
        description_dict = json.load(json_file)

    html = description_dict['html_description']
    soup = BeautifulSoup(html, 'html.parser')

    product_id = get_id(descr_page)
    group = description_dict['group']
    name = get_name(soup)
    comments = get_comment(soup)
    image_link = get_image(soup)
    descr = description(soup)
    addition = toppings(soup)
    price = product_price(soup)
    weight = product_weight(soup)

    v_count, v_product = vars_product(soup)

    with open('/home/vyacheslav/parsing/kfc/html_garbage/{}'.format(struct_page)) as json_file:
        structure_dict = json.load(json_file)

    html = structure_dict['html_structure']
    soup = BeautifulSoup(html, 'html.parser')
    structure = consistency(soup)
    kcal = calories(soup)
    pfc = proteins(soup)

    element = {
        'id': product_id,
        'group': group,
        'name': name,
        'comment': comments,
        'image': image_link,
        'descr': descr,
        'consistency': structure,
        'kcal': kcal,
        'pfc': pfc,
        'additions': addition,
        'price': price,
        'weight': weight,
        'vars_count': v_count
    }

    c = 0
    for k, v in v_product.items():
        c += 1
        element['var_{}'.format(c)] = k
        element['price_{}'.format(c)] = v

    if element not in elements:
        elements.append(element)

with open('/home/vyacheslav/parsing/kfc/kfc.json', 'w', encoding='utf-8') as fd:
    json.dump(elements, fd)
