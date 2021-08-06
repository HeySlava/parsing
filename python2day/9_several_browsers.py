from fake_useragent import UserAgent
from multiprocessing import Pool
from selenium import webdriver
import datetime
import random
import time

options = webdriver.ChromeOptions()
useragent = UserAgent().random

# options.add_argument(f"user-agent={useragent}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("headless")
# options.headless = True
urls_list = ['https://vk.com', 'https://instagram.com', 'https:stepic.org']
urls_list = ['https://tiktok.com']

link = 'https://www.avito.ru/tula?q=%D0%B3%D0%B8%D1%80%D1%8F+16+%D0%BA%D0%B3'

# def get_data(url):

#     driver = webdriver.Chrome(
#             executable_path=r"/usr/bin/chromedriver",
#             options=options
#     )

#     try:
#         name = url.split('//')[1]
#         print(url)
#         print(name)
#         driver.get(url=url)
#         time.sleep(10)
#         driver.get_screenshot_as_file(filename=f"./media/{name}.png")

#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.quit()



def get_data(url):
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("headless")

    driver = webdriver.Chrome(
            executable_path=r"/usr/bin/chromedriver",
            options=options
    )

    try:
        print(url)
        name = url.split('//')[1]
        driver.get(url=url)
        time.sleep(random.randrange(1, 3))
        driver.get_screenshot_as_file(filename=f"./media/{name}.png")

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()

if __name__ =='__main__':
    print('enter number of cites')
    count = int(input())
    p = Pool(processes=2)
    p.map(get_data, urls_list * count)

