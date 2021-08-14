from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from vk_auth  import login, password
import random
import time
import pickle

options = webdriver.ChromeOptions()
useragent = UserAgent().random

options.add_argument(f"user-agent={useragent}")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("headless")
options.headless = True

driver = webdriver.Chrome(
        executable_path=r"/usr/bin/chromedriver",
        options=options
)

# link = 'https://prodoctorov.ru/podolsk/lpu/34291-zhemchuzhina-podolya/otzivi/'
link = 'https://vk.com/'

try:
    driver.get(link)
    time.sleep(1)

    email_input = driver.find_element_by_id('index_email')
    email_input.clear()
    email_input.send_keys(login)
    time.sleep(1)
    print('input login')

    password_input = driver.find_element_by_id('index_pass')
    password_input.clear()
    password_input.send_keys(password)
    print('input password')
    time.sleep(1)
    password_input.send_keys(Keys.ENTER)
    print('entered to account')

    time.sleep(5)

    my_page = driver.find_element_by_id('l_pr').click()
    time.sleep(1)
    print('click on my page')

    page_video = driver.find_element_by_css_selector('.post_video_title').click()
    print('click on video')
    time.sleep(13)
    print('stop watching video')

except Exception as ex:
    print(ex)
finally:
    driver.quit()


