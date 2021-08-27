import json
import requests
from datetime import datetime


def get_data():

    r = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    responce = r.json()
    sell_price = responce['btc_usd']['sell']
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price : {sell_price}")


if __name__ == '__main__':
    get_data()

