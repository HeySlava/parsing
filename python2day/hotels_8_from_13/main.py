from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
import time


def get_data(url):
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)

    with open("index.html", "w") as file:
        file.write(r.text)

    with open("index.html", 'r') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    hotels_list = soup.select('.hotel_card_dv')
    hotels_href = [hotel.select_one('a')['href'] for hotel in hotels_list]


def get_data_with_selenium(url=None):

    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("headless")
    # options.headless = True

    try:

        driver = webdriver.Chrome(
                        executable_path=r"/usr/bin/chromedriver",
                                options=options)

        driver.get(url)
        time.sleep(5)

        with open('index_selenium.html', 'w') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


def main():
    old_url = "https://www.tury.ru/hotel/most_luxe.php"
    new_url = "https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most&"
    # get_data(new_url)
    get_data_with_selenium(url=new_url)

if __name__ == '__main__':
    main()
