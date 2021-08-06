from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path=r"/home/vyacheslav/.config/JetBrains/PyCharm2020.3/scratches/chromedriver")

driver.set_window_size(1500, 768)

city = 'moscow'
link = 'https://sushiport.ru/{}/index.php?route=product/category&path=72'.format(city)

driver.get(link)

try:
    time.sleep(2)
    chapters = driver.find_elements_by_css_selector('.box-category li')
    links = []
    for chapter in chapters:
        links.append(chapter.find_element_by_css_selector('a').get_attribute('href'))

    link_products = []
    for link in links:
        driver.get(link)
        images = driver.find_elements_by_css_selector('.image a')
        for img in images:
            link_products.append(img.get_attribute('href'))
        time.sleep(2)

    for product in link_products:
        time.sleep(2)
        driver.get(product)
        html = driver.page_source
        place = product.find('product_id=')
        product_id = product[place:].replace('product_id=', '')
        with open('/home/vyacheslav/parsing/sushiport/html_garbage_{}/{}.txt'.format(city, product_id), 'w') as file:
            file.write(html)

finally:
    driver.quit()
    print('Мне кажется что это задача уже выполнена')
