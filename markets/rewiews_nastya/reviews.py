from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import json
import time


def get_info_from_page(sp, req, quantity=1, href=None):
    if href:
        product_info = sp.select_one(req)
        if product_info:
            product_info = product_info['href']
            product_info = 'https://prodoctorov.ru/' + product_info
    else:
        if quantity == 1:
            product_info  = sp.select_one(req)
            if product_info:
                product_info = product_info.text.strip()
        else:
            product_info  = sp.select(req)
            if product_info:
                product_info = [el.text.strip() for el in product_info]
    return product_info


useragent = UserAgent().random

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent}")

# options.add_argument("--proxy-server=176.62.178.247:47556")

driver = webdriver.Chrome(
        executable_path=r"/usr/bin/chromedriver",
        options=options
    )

link = "https://2ip.ru/"
link = 'https://prodoctorov.ru/podolsk/lpu/34291-zhemchuzhina-podolya/otzivi/'

try:
    driver.get(link)
    time.sleep(3)

    count = 1
    next_buttom = driver.find_elements_by_css_selector('.ui-text.ui-text_button.ui-text_color_neur-blue')
    while len(next_buttom) != 0:
        next_buttom[0].click()
        print(f"I refreshed this page {count} times")
        next_buttom = driver.find_elements_by_css_selector('.ui-text.ui-text_button.ui-text_color_neur-blue')
        count += 1
        time.sleep(2)
        page = driver.page_source

except Exception as ex:
    print(ex)

finally:

    with open("full_page.html", 'w') as f:
        f.write(page)

    driver.quit()

with open("full_page.html") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")

block_of_comments = soup.select('.b-review-card')
all_data = []
count = 1
total = len(block_of_comments)
for item in block_of_comments:

    author = get_info_from_page(item, '.b-review-card__author-name')
    rating = get_info_from_page(item, '.b-review-card__rate-num')
    rating_name = get_info_from_page(item, '.b-review-card__rate-name')
    comments_title = get_info_from_page(item, '.b-review-card__comment-title', 2)
    comments = get_info_from_page(item, '.b-review-card__comment', 2)
    title_and_comments = dict(zip(comments_title, comments))
    adress = get_info_from_page(item, '.b-review-card__address')
    date_comment = get_info_from_page(item, '.b-review-card__datetime')
    doctor = get_info_from_page(item, '.ui-text_color_neur-blue')
    # print(author, rating, rating_name, comments_title, comments, adress, date_comment)
    doctor_href = get_info_from_page(item, '.mt-4 .ui-text_color_neur-blue', quantity=1, href=True)

    all_data.append(
            {
                'author': author,
                'rating': rating,
                'rating_name': rating_name,
                'title_and_comments': title_and_comments,
                'adress': adress,
                'date_comment': date_comment,
                'doctor': doctor,
                'doctro_href': doctor_href
            }
        )

    print(f"Done {count} / {total}")
    count += 1


with open('anastasia.json', 'w') as file:
    json.dump(all_data, file, indent=4, ensure_ascii=False)

