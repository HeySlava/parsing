from bs4 import BeautifulSoup
import json
import requests
import time


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

for i in range(0, 24, 168):
    print(i)

    # url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=10%20Aug%202021&to_date=&maxprice=500&o={i}&bannertitle=August'
