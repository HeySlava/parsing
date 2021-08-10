from bs4 import BeautifulSoup
import json
import json
import requests
import time
import os


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

# for i in range(0, 168, 24):
#     url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=10%20Aug%202021&to_date=&maxprice=500&o={i}&bannertitle=August'
#     req = requests.get(url=url, headers=headers)
#     json_data = json.loads(req.text)
#     html_response = json_data['html']

#     with open(f'data/index_{i}.html', 'w') as f:
#         f.write(html_response)
#     print(f'Saved {i + 24} from 168')
#     time.sleep(1)

festival_hrefs = []
files = os.listdir('data/')
for page in files:

    with open(f'data/{page}') as file:
        src = file.read()
        soup = BeautifulSoup(src, 'lxml')

    domen = 'https://www.skiddle.com/'
    festival_hrefs.extend(
            [domen + l['href'] for l in soup.select('.card a')]
            )

for url in set(festival_hrefs):
    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, 'lxml')

        festival_name = soup.select_one('div h1').text.strip()
        festival_date = soup.select_one('div h3').text.strip()
        festival_accommodation = domen + soup\
                .select_one('.p-13pt a.tc-white')['href'].strip()

        req = requests.get(url=festival_accommodation, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        additional_info = soup\
                .select('.margin-bottom-20 p.no-top-margin')
        add_info_dict = {}
        for i in additional_info:
            k_v = i.text.split(':')
            if len(k_v) != 2:
                k = k_v[0].strip()
                v = ''.join(k_v[1:]).strip()
            else:
                k = k_v[0].strip()
                v = k_v[1].strip()
            add_info_dict[k] = v

        print(add_info_dict)


    except Exception as ex:
        print(ex)

    # finally:
    break



