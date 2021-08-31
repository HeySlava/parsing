import time
from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
useragent = UserAgent().random

# options.add_argument(f"user-agent={useragent}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
        executable_path="./chromedriver",
        options=options
)

# options.add_argument("headless")
# driver = webdriver.Chrome(ChromeDriverManager().install(),
#         options=options)

# link = 'https://prodoctorov.ru/podolsk/lpu/34291-zhemchuzhina-podolya/otzivi/'
link = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'

try:
    driver.get(link)
    time.sleep(10)
except Exception as ex:
    print(ex)
finally:
    driver.quit()

