import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ContentType
from asgiref.sync import sync_to_async

from server.models import TGUser

about = '''Earn cryptocurrency by subscribing to the best Telegram channels!

Welcome to the world of earning with our new Telegram Mini App! Want to earn cryptocurrency just by subscribing to interesting and useful Telegram channels? Now it's possible!

Our app allows you to earn TON cryptocurrency for every subscription. Choose from a variety of channels on different topics: news, sports, technology, entertainment, and much more. The more you subscribe, the more you earn!

Why should you try our app?

Simplicity and convenience: No complications! Just open the app, select interesting channels, and subscribe.
Great rewards: Earn cryptocurrency for every subscription. You choose how many channels to subscribe to and which ones.
Exclusive offers: Be the first to discover new channels and get more opportunities to earn.
Complete security: We care about your safety and privacy. All transactions are conducted through secure channels.
Start earning TON now! Discover new channels, learn a lot of new and interesting things, and earn money doing it. Join our growing community and start your journey to financial independence with cryptocurrency!'''

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = '7241869710:AAG3HyzczGxHwxQmetXRKvjMWo9wyNqqyr0'
URL = 'https://young-paws-tap.loca.lt'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# conn = sqlite3.connect('/home/vitaly-vitaly/projects/python/subs/server/subs_server/db.sqlite3')
# cursor = conn.cursor()


@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def handle_web_app_data(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"Received data from Web App: {data}")


@dp.message()
async def start(message: types.Message):
    user_exists = await sync_to_async(TGUser.objects.filter(tg_id=message.from_user.id).exists)()
    if not user_exists:
        user = TGUser()
        user.tg_id = message.from_user.id
        user.chat_id = message.chat.id
        user.tg_username = message.from_user.username
        user.ton_balance = 0.0
        user.scribe_balance = 0
        await sync_to_async(user.save)()
    web_app_info = types.WebAppInfo(url=URL)
    button1 = InlineKeyboardButton(text='Play in 1 click', web_app=web_app_info)
    button2 = InlineKeyboardButton(text='How to play', callback_data='how_to_play')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, ], [button2,]])
    await message.answer('Welcome!', reply_markup=keyboard)

    # webAppInfo = types.WebAppInfo(url="https://google.com")
    # builder = ReplyKeyboardBuilder()
    # builder.add(types.KeyboardButton(text='Старт', web_app=webAppInfo))
    #
    # await message.answer(text='Привет!', reply_markup=builder.as_markup())


#
# @dp.message(commands=['invite_link'])
# async def send_invite_link(message: types.Message):
#     try:
#         invite_link = await bot.export_chat_invite_link(chat_id=CHAT_ID)
#         await message.answer(f"Here is your invite link: {invite_link}")
#     except Exception as e:
#         await message.answer(f"An error occurred: {e}")


@dp.callback_query(lambda c: c.data == 'how_to_play')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, about)


@dp.callback_query(lambda c: c.data == 'register')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "hm")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def is_subscribe(offer_name, tg_id):
    channel_id = '@' + offer_name
    print(channel_id)
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=tg_id)
        if member.status in ['member', 'administrator', 'creator']:
            print("You are a member of the channel.")
        else:
            print("You are not a member of the channel.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
