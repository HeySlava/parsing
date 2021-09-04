import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from tg_auth import token


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(Text(equals="start"))
async def start(message: types.Message):
    start_buttons = ["Last 5 from fl.ru", "Last 5 from youdo.com"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("The data is automatically refreshed every 5 minutes.", reply_markup=keyboard)


@dp.message_handler(Text(equals="a"))
async def random(message: types.Message):

    with open('data/news_dict.json', encoding='utf-8') as file:
        news = json.load(file)

    for k, v in news.items():
        title, link = v
        # link = f"{hlink(title, link)}"
        await message.answer(f"{hlink(title, link)}")


async def news_every_minute():
    while True:

        with open('data/news_dict.json', encoding='utf-8') as file:
            news = json.load(file)

        for k, v in news.items():
            title, link = v
            # link = f"{hlink(title, link)}"
            await bot.send_message(user_id, f"{hlink(title, link)}")

        await asyncio.sleep(20)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)


