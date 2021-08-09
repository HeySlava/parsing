from bs4 import BeautifulSoup
import requests
import time

# persons_link = []
# for i in range(0, 740, 20):
#     url = f"https://www.bundestag.de/ajax/filterlist/en/members/453158-453158/h_a45203fd0f1592191f1bda63b5d86d72?limit=20&noFilterSet=true&offset={i}"

#     q = requests.get(url)
#     result = q.content

#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.select('.bt-slide-content a')

#     for person in persons:
#         persons_link.append(person.get('href'))
#     time.sleep(1)
#     print(i)

# with open('candidate_links.txt', 'a') as f:
#     for person in persons_link:
#         f.write(f'{person}\n')

with open('candidate_links.txt') as f:
    links = [link.strip() for link in f.readlines()]

count = 0
for url in links:
    q = requests.get(url)
    # soup = BeautifulSoup(q.content, 'lxml')

    # name = soup.select_one('.bt-biografie-beruf p').text

    count += 1
    with open(f'data/{count}', 'w') as f:
        f.write(q.text)

    print(f"Done {count} from {len(links)}")
    time.sleep(0.5)

