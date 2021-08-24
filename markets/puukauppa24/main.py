# from bs4 import BeautifulSoup
import csv
import datetime
import json
import lxml
import os
import requests
import time

if not os.path.isdir('data/'):
    os.mkdir('data')

def get_city_links():
    url = 'https://www.puukauppa24.fi/puukaupat/'

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    city_content = soup.select('.kaikki-kaupungit .page_item a')
    city_name = [name.text for name in city_content]
    city_link = [link['href'] for link in city_content]

    with open('data/city_link.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
                (
                    "City",
                    "link"
                )
            )

    for city, link in zip(city_name, city_link):
        with open('data/city_link.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                    (
                        city,
                        link
                    )
                )


def get_city_page():

    if not os.path.exists('data/city_pages'):
        os.mkdir('data/city_pages')

    total = 0
    with open('data/city_link.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        for i in reader:
            total += 1

    with open('data/city_link.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)

        count = 0
        data = []
        for city, url  in reader:
            r = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            count += 1

            data.append(
                        {
                            'city_name': city,
                            'html': r.text
                        }
                    )

            with open(f'data/city_pages/{city}.html', 'w') as file:
                file.write(r.text)

            print(f'[INFO] City {count}/{total}')
            time.sleep(0.25)

        with open(f'data/city_pages.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def get_shops():

    if not os.path.exists('data/shop_pages'):
        os.mkdir('data/shop_pages')

    # with open(f'data/city_shop_link.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(
    #             (
    #                 'City',
    #                 'Shop',
    #                 'Link'
    #             )
    #         )

    # with open('data/city_pages.json') as file:
    #     pages = json.load(file)

    # for item in pages:

    #     city_name = item['city_name']
    #     soup = BeautifulSoup(item['html'], 'lxml')

    #     shop_links = soup.select('.kaupunki a')
    #     city_shop_link = []
    #     for shop in shop_links:
    #         city_shop_link.append(
    #                 (
    #                     city_name,
    #                     shop.text,
    #                     'https://www.puukauppa24.fi' + shop['href']
    #                 )
    #             )

    #         with open(f'data/city_shop_link.csv', 'a') as file:
    #             writer = csv.writer(file)
    #             writer.writerow(
    #                     (
    #                         city_name,
    #                         shop.text,
    #                         'https://www.puukauppa24.fi' + shop['href']
    #                     )
    #                 )

    with open('data/city_shop_link.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        total = 0
        for i in reader:
            total += 1

    with open('data/city_shop_link.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)

        count = 0
        data = []
        for city, shop, url  in reader:
            r = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            count += 1

            data.append(
                        {
                            'city_name': city,
                            'shop_name': shop,
                            'html': r.text
                        }
                    )

            with open(f'data/shop_pages/{count}.html', 'w') as file:
                file.write(r.text)

            print(f'[INFO] Shop {count}/{total}')
            time.sleep(0.25)
            # break

        with open(f'data/city_shop_pages.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def get_shop_info():

    with open('data/final.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
                (
                    "City",
                    "Shop",
                    "phone",
                    "email"
                )
            )

    files = os.listdir('data/shop_pages')

    data = []
    count = 0
    for file_name in files:
        with open(f'data/shop_pages/{file_name}') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        content = soup.select('.entry-content b')

        info = dict()
        for name in content:
            info[name.text.strip()[:-1]] = name.next_element.next_element.strip()

        data.append(info)
        count += 1
        if count % 50 == 0:
            print(f'Final step {count} / {len(files)}')

        # break
    with open('data/final.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    for item in data:

        if 'Puukaupan nimi' in item:
            shop_name = item['Puukaupan nimi']
        else:
            phone = 'null'

        if 'Sähköpostiosoite' in item:
            email = item['Sähköpostiosoite']
        else:
            email = 'null'

        if 'Puhelinnumero' in item:
            phone = item['Puhelinnumero']

            if phone.startswith('0'):
                phone = '+358' + phone[1:]
        else:
            phone = 'null'

        if 'Osoite' in item:
            city_string = item['Osoite']
            city = city_string.split()[-1]
        else:
            city = 'null'

        with open('data/final.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                    (
                        city,
                        shop_name,
                        phone,
                        email
                    )
                )
        # break



if __name__ == '__main__':
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }

    # get_city_links()
    # get_city_page()
    # get_shops()
    get_shop_info()

