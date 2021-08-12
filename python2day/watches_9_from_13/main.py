from bs4 import BeautifulSoup
import lxml
import os
import requests


def get_all_pages():
    # headers = {
    #         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

    # r = requests.get(url="https://shop.casio.ru/catalog/g-shock/",
    #                  headers=headers)

    # if not os.path.exists('data'):
    #     print('This folder is not exists')
    #     os.mkdir('data')

    # with open('data/page_1.html', 'w') as file:
    #     file.write(r.text)

    with open('data/page_1.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    page_count = soup.select_one('.bx-pagination-container li').text
    print(page_count)


def main():
    get_all_pages()


if __name__ == '__main__':
    main()
