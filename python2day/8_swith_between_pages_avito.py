from fake_useragent import UserAgent
from selenium import webdriver
import time
import datetime

options = webdriver.ChromeOptions()
useragent = UserAgent().random

# options.add_argument(f"user-agent={useragent}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("headless")
# options.headless = True

driver = webdriver.Chrome(
        executable_path=r"/usr/bin/chromedriver",
        options=options
)

link = 'https://www.avito.ru/tula?q=%D0%B3%D0%B8%D1%80%D1%8F+16+%D0%BA%D0%B3'

try:
    start_time = datetime.datetime.now()

    driver.get(link)
    time.sleep(2)
    # driver.implicitly_wait(10)
    elements = driver.find_elements_by_css_selector('h3.iva-item-title-1Rmmj')
    time.sleep(1)
    # driver.implicitly_wait(10)

    elements[0].click()
    time.sleep(10)
    # driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    # driver.implicitly_wait(10)

    price = driver.find_element_by_css_selector('.item-price-wrapper .price-value-string')
    price = price.text.strip()

    title = driver.find_element_by_css_selector('.title-info-title-text')
    title = title.text.strip()

    print(title)
    print(price)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    elements[1].click()
    time.sleep(5)
    # driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    # driver.implicitly_wait(10)

    price = driver.find_element_by_css_selector('.item-price-wrapper .price-value-string')
    price = price.text.strip()

    title = driver.find_element_by_css_selector('.title-info-title-text')
    title = title.text.strip()

    print(title)
    print(price)

    finish_time = datetime.datetime.now()

    print(finish_time - start_time)

except Exception as ex:
    print(ex)
finally:
    driver.quit()



