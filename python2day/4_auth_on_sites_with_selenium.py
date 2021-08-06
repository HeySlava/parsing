from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from vk_auth  import login, password
import random
import time

options = webdriver.ChromeOptions()
useragent = UserAgent().random
options.add_argument(f"user-agent={useragent}")

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

    password_input = driver.find_element_by_id('index_pass')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(1)
    password_input.send_keys(Keys.ENTER)

    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.quit()
