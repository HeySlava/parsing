from bs4 import BeautifulSoup
import os

files = os.listdir(r'/home/vyacheslav/parsing/wok/html_pages/')
print(files)

for file in files:
    with open(r'/home/vyacheslav/parsing/wok/html_pages/{}'.format(file)) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')


    dishes = soup.select('.card-wrapper--grid')
    print(len(dishes))
    for el in dishes:
        data_id = el.find('a')['data-id']

        photo = el.select_one('.card__image_container').find('img')
        title, photo_link = photo['title'], photo['src']

        main_content = el.select_one('.card__ingredients')
        ingredients = main_content.getText()
        weight = main_content.find('span').getText()

        # print(main_content)
        print(photo)
        print(title, photo_link, data_id, ingredients, weight, sep='\n')
        print()
