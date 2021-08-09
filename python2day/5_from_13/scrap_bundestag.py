import requests
from bs4 import BeautifulSoup


for i in range(0, 740, 20):
    url = f"https://www.bundestag.de/ajax/filterlist/en/members/453158-453158/h_a45203fd0f1592191f1bda63b5d86d72?limit=20&noFilterSet=true&offset={i}"
    print(url)

