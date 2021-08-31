import random
from aiogram import Bot, Dispatcher, executor, types
from news_bot_token import token
import json


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("my answer on first message")

@dp.message_handler(commands="random")
async def random(message: types.Message):
    await message.reply('Slava')
    with open('data/news_dict.json', encoding='utf-8') as file:
        news = json.load(file)

    for k, v in news.items():

        # print(v)
        title, link = v
        # print(title, link)
        await message.reply(f"{link}")


if __name__ == '__main__':
    executor.start_polling(dp)

