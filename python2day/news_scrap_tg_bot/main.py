import json
import lxml
import os
import requests

from bs4 import BeautifulSoup


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
def get_first_news():

    if not os.path.exists('data'):
        os.mkdir('data')

    url = 'https://www.bellingcat.com/category/resources/case-studies/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    article_cards = soup.select('.news_item')
    title_link_img_list = {
            item.select_one('img')['src']:
            (
                item.select_one('h3 a').text.strip(),
                item.select_one('h3 a')['href']
            )
            for item in article_cards
        }

    with open("data/news_dict.json", "w") as file:
        json.dump(title_link_img_list, file, indent=4, ensure_ascii=False)


def check_news_update():

def main():
    get_first_news()


if __name__ == '__main__':
    main()

