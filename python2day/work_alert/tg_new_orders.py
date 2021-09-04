import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from data.tg_auth import token


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Last 5 from fl.ru", "Last 5 from youdo.com"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("The data is automatically refreshed every 5 minutes.", reply_markup=keyboard)


@dp.message_handler(Text(equals="Last 5 from fl.ru"))
async def random(message: types.Message):

    with open('data/posts.json', encoding='utf-8') as file:
        news = json.load(file)
    news = sorted(news, reverse=True, key=lambda news: news['items']['unix'])
    for item in news[:5]:
        await message.answer(f"{item['items']}")


@dp.message_handler(Text(equals="Last 5 from youdo.com"))
async def random(message: types.Message):
    pass


# async def news_every_minute():
#     while True:

#         with open('data/news_dict.json', encoding='utf-8') as file:
#             news = json.load(file)

#         for k, v in news.items():
#             title, link = v
#             # link = f"{hlink(title, link)}"
#             await bot.send_message(user_id, f"{hlink(title, link)}")

#         await asyncio.sleep(20)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(news_every_minute())
    # executor.start_polling(dp)
    executor.start_polling(dp)

