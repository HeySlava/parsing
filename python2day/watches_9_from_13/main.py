from bs4 import BeautifulSoup
import csv
import datetime
import json
import lxml
import os
import requests
import time


def get_all_pages():

    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

    # r = requests.get(url="https://shop.casio.ru/catalog/g-shock/",
    #                  headers=headers)

    if not os.path.exists('data'):
        print('This folder is not exists')
        os.mkdir('data')

    # with open('data/page_1.html', 'w') as file:
    #     file.write(r.text)

#     with open('data/page_1.html') as file:
#         src = file.read()

#     soup = BeautifulSoup(src, 'lxml')
#     page_count = int(soup.select('.bx-pagination-container li a')[-2].text)

#     for page in range(1, page_count + 1):
#         url = f'https://shop.casio.ru/catalog/g-shock/?PAGEN_1={page}'

#         r = requests.get(url=url, headers=headers)

#         with open (f'data/page_{page}.html', 'w') as file:
#             file.write(r.text)

#         time.sleep(1)
#         print(f'Done {page}/{page_count}')

#     return page_count + 1


def collect_data():

    cur_date = datetime.datetime.now().strftime("%d_%m_%Y")
    pages = os.listdir('data')

    with open(f"data_{cur_date}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
                (
                    "Артикул",
                    "Ссылка",
                    "Цена"
                )
            )

    watches = []
    data = []
    for page in pages:
        with open(f'data/{page}') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')

        watches.extend(soup.select('.product-item'))

    for item in watches:

        article = item.select_one('.product-item__articul').text.strip()
        price = item.select_one('.product-item__price').text.strip()\
                .lstrip("руб.").replace(' ', '')
        href = 'https://shop.casio.ru/' + \
                item.select_one('a')['href'].strip()

        data.append(
                {
                    "article": article,
                    "price": price,
                    "href": href
                }
            )

        with open(f"data_{cur_date}.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                    (
                        article,
                        price,
                        href
                    )
                )

    with open(f'data_{cur_date}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    # pages_count = get_all_pages()
    collect_data()


if __name__ == '__main__':
    main()
