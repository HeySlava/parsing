from bs4 import BeautifulSoup
import csv
import json
import re
import requests
import time

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
        "Access-Control-Allow-Origin": "*",
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w") as file:
#     file.write(src)

# with open("./order_two/index.html") as file:
#     src = file.read()
# soup = BeautifulSoup(src, "lxml")

# all_categories_dict = {}
# rep = ["'", "-", " ", ".", ","]
# all_products = soup.select('.mzr-tc-group-item-href')

# count = 0
# for product in all_products:
#     product_href = 'https://health-diet.ru' + product['href']
    # product_text = product.text.strip()   

    # for item in rep:
    #     if item in product_text:
    #         product_text = product_text.replace(item, '_')
    # product_text = f"{count}_" + product_text
    # all_categories_dict[product_text] = product_href
    # count += 1

# with open('./order_two/all_categories_dict.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('./order_two/all_categories_dict.json',) as file:
    all_category = json.load(file)
all_category_name = [name for name in all_category]
count = len(all_category)

# for category_name, category_ref in all_category.items():
#     req = requests.get(url=category_ref, headers=headers)
#     src = req.text

#     with open(f"./order_two/data/{category_name}.html", 'w') as file:
#         file.write(src)
#     time.sleep(1)
#     print(f"Осталось сделать запросов {count}")
#     count -= 1

for name in all_category_name:

    print(name)
    if 'Danone' in name:
        continue

    with open(f"./order_two/data/{name}.html") as file:
        soup = BeautifulSoup(file.read(), "lxml")

        all_together = soup.select('thead tr th')
        title = all_together[0].text.strip()
        calories = all_together[1].text.strip()
        proteins = all_together[2].text.strip()
        fats = all_together[3].text.strip()
        carbohydrates = all_together[4].text.strip()

    with open(f"./order_two/data/{name}.csv", 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

        all_together = soup.select('.uk-margin-top tbody tr')
        product_on_page_json = []
        for product in all_together:
            info = product.find_all('td')

            title = info[0].text.strip()
            calories = info[1].text.strip()
            proteins = info[2].text.strip()
            fats = info[3].text.strip()
            carbohydrates = info[4].text.strip()

            product_on_page_json.append(
                    {
                        'title': title,
                        'calories': calories,
                        'proteins': proteins,
                        'fats': fats,
                        'carbohydrates':carbohydrates
                    }
                )

            with open(f"./order_two/data/{name}.csv", 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                        (
                            title,
                            calories,
                            proteins,
                            fats,
                            carbohydrates
                        )
                    )
        with open(f"./order_two/data/{name}.json", "a", encoding='utf-8') as f:
            json.dump(product_on_page_json, f, indent=4, ensure_ascii=False)


    # break












