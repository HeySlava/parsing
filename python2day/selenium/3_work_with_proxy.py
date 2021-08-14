from selenium import webdriver
import time
import random
from fake_useragent import UserAgent
from proxy_auth_data import login, password

user_agent_list = [
        "hello_world",
        "best_of_the_best"
]

options = webdriver.ChromeOptions()
useragent = UserAgent()
options.add_argument(f"user-agent={useragent}")
# options.add_argument("--proxy-server=213.79.122.108:8080")

driver = webdriver.Chrome(
        executable_path=r"/usr/bin/chromedriver",
        options=options
)

link = 'https://prodoctorov.ru/podolsk/lpu/34291-zhemchuzhina-podolya/otzivi/'

