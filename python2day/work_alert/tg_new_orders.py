import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from freelance import update_posts, get_data
from data.tg_auth import token, user_id


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Last 5 from fl.ru", "Last 5 from youdo.com"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("The data is automatically refreshed every 30 minutes.", reply_markup=keyboard)


@dp.message_handler(Text(equals="Last 5 from fl.ru"))
async def random(message: types.Message):

    with open('data/posts.json', encoding='utf-8') as file:
        news = json.load(file)
    for item in news[5::-1]:
        time = item['items']['time']
        title = item['items']['title']
        href = item['items']['href']
        description = item['items']['description']
        price  = item['items']['price']
        await message.answer(
                f"{hbold(time)}\n"\
                f"{price}\n"\
                f"{description}\n"\
                f"{href}\n"\
                    )


@dp.message_handler(Text(equals="Last 5 from youdo.com"))
async def random(message: types.Message):
    await message.answer('I have not done it yet')


async def news_every_minute():
    while True:

        new_posts = update_posts(get_data())

        if new_posts:
            for item in new_posts:
                time = item['items']['time']
                title = item['items']['title']
                href = item['items']['href']
                description = item['items']['description']
                price  = item['items']['price']
                await bot.send_message(user_id,
                        f"{hbold(time)}\n"\
                        f"{price}\n"\
                        f"{description}\n"\
                        f"{href}\n"\
                            )

        await asyncio.sleep(60* 60)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)

