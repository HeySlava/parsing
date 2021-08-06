from selenium import webdriver

from fake_useragent import UserAgent 
import time
import json

useragent = UserAgent().random

options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={useragent}")

options.add_argument("--proxy-server=89.208.35.79:60358")
driver = webdriver.Chrome(
        executable_path=r"/usr/bin/chromedriver",
        options=options
    )

link = "https://2ip.ru/"
link = 'https://prodoctorov.ru/podolsk/lpu/34291-zhemchuzhina-podolya/otzivi/'

try:
    driver.get(link)
    time.sleep(10)
finally:
    driver.quit()

