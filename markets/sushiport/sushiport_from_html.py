import json
import re
from bs4 import BeautifulSoup
import os
import requests

print('Введи moscow, samara or tula')
city = input()
files = os.listdir('/home/vyacheslav/parsing/sushiport/html_garbage_{}'.format(city))

final_data = []

for file in files:
    if '.txt' in file:

        with open('/home/vyacheslav/parsing/sushiport/html_garbage_{}/{}'.format(city, file)) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

            levels = soup.select_one('.breadcrumb')
            # print(file)
            links = levels.findAll('a')

            name = soup.select_one('h1').getText()

            image = soup.select_one('.image').find('img')['src']
            image = image.replace(' ', '%20')

            price = soup.select_one('.price').getText()
            # price = price.replace('Цена:                ', '')
            price = re.findall('[0-9]+', price)[0]

            descr = soup.select_one('.tab-content').find('p').getText()
            # weight = re.findall('\((.+)\)', descr)
            weight = re.findall('\d+.{2}', descr)
            if len(weight) > 0:
                weight = weight[-1]
            elif len(weight) == 0:
                weight = None
            bracket = descr.find('(')
            descr = descr[:bracket]
            if descr.replace('\xa0', '') == '':
                descr = None

            options = {}

            if city == 'moscow':
                additions = soup.select('.option label')
                # print(additions)
                for addition in additions:
                    addition = addition.getText()
                    addition = addition.split('(')
                    add_name = addition[0].strip()
                    add_value = addition[-1].strip()[1:-3]
                    # print(add_name, add_value)
                    options[add_name] = add_value
                    # description = addition.getText()
                    # print(description)
            else:
                additions = soup.select('.col-md-6')
                for addition in additions:
                    description = addition.find('img')['alt']
                    add_price = re.findall('[0-9]+', description)[0]
                    add_name = description.split('+')[0].strip()
                    options[add_name] = add_price

            if not options:
                options = None

            if len(links) == 4:
                group = links[1].getText()
                subgroup = links[2].getText()

            if len(links) == 3:
                group = links[1].getText()
                subgroup = None

            one_element = {
                'id': file[:-4],
                'group': group,
                'subgroup': subgroup,
                'name': name,
                'image': image,
                'price': price,
                'descr': descr,
                'weight': weight,
                'additions': options
            }
    if one_element not in final_data:
        final_data.append(one_element)


        # print(group)
        # print(subgroup)
        # print(name)
        # print(image)
        # print(price)
        # print(descr)
        # print(*weight)
        # print(options)

with open('/home/vyacheslav/parsing/sushiport/sushiport_{}.json'.format(city), 'w', encoding='utf-8') as fd:
    json.dump(final_data, fd)

# quality = {}
# for i in final_data:
#     print(i['image'])
#     test = requests.get(i['image']).status_code
#     if test not in quality:
#         quality[test] = 0
#     quality[test] += 1
# print(quality)
