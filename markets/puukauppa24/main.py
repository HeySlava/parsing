from bs4 import BeautifulSoup
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

            print(f'[INFO] Done {count}/{total}')
            # time.sleep(0.15)

        with open(f'data/city_pages.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }

    # get_city_links()
    # get_city_page()

