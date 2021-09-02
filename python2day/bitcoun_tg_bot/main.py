import json
import requests
import telebot
from datetime import datetime
from bitcoin_bot_token import token


def get_data():

    r = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    responce = r.json()
    sell_price = responce['btc_usd']['sell']
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price : {sell_price}"



def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Write the 'price' to find out the cost of BTC")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price":
            try:
                bot.send_message(message.chat.id,
                        get_data()
                    )
            except Exception as ex:
                print(ex)
                bot.send_message(
                        massage.chat.id,
                        "Damn...Something was wrong"
                    )
        else:
             bot.send_message(message.chat.id, "This bot support only 'price' message")
    bot.polling()

if __name__ == '__main__':
    # get_data()
    telegram_bot(token)

