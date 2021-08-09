from bs4 import BeautifulSoup
import requests
import time

persons_link = []
for i in range(0, 740, 20):
    url = f"https://www.bundestag.de/ajax/filterlist/en/members/453158-453158/h_a45203fd0f1592191f1bda63b5d86d72?limit=20&noFilterSet=true&offset={i}"

    q = requests.get(url)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')
    persons = soup.select('.bt-slide-content a')

    for person in persons:
        persons_link.append(person.get('href'))
    time.sleep(1)

with open('candidate_links.txt', 'a') as f:
    for person_link in persons_link:
        f.write(f'{person}\n')

