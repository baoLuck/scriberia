import asyncio
import logging

import httpx
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ContentType, InlineKeyboardButton, InlineKeyboardMarkup

# TODO: remove dependencies from other service
from django.conf import settings

about = """
Earn cryptocurrency by subscribing to the best Telegram channels!

Welcome to the world of earning with our new Telegram Mini App! Want to earn cryptocurrency just by subscribing to
interesting and useful Telegram channels? Now it's possible!

Our app allows you to earn TON cryptocurrency for every subscription. Choose from a variety of channels on different
topics: news, sports, technology, entertainment, and much more. The more you subscribe, the more you earn!

Why should you try our app?

Simplicity and convenience: No complications! Just open the app, select interesting channels, and subscribe.
Great rewards: Earn cryptocurrency for every subscription. You choose how many channels to subscribe to and which ones.
Exclusive offers: Be the first to discover new channels and get more opportunities to earn.
Complete security: We care about your safety and privacy. All transactions are conducted through secure channels.
Start earning TON now! Discover new channels, learn a lot of new and interesting things, and earn money doing it.
Join our growing community and start your journey to financial independence with cryptocurrency!
"""

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TG_BOT_API_TOKEN)
dp = Dispatcher()

logger = logging.getLogger(__name__)


@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def handle_web_app_data(message: types.Message):
    await message.answer(f"Received data from Web App: {message.web_app_data.data}")


@dp.message()
async def start(message: types.Message):
    async with httpx.AsyncClient() as client:
        await client.put(
            url="https://tidy-paws-clap.loca.lt/users/",
            data={
                "tg_id": message.from_user.id,
                "chat_id": message.chat.id,
                "tg_username": message.from_user.username,
            },
        )

    web_app_info = types.WebAppInfo(url=settings.SERVER_URL)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Play in 1 click", web_app=web_app_info),
            ],
            [
                InlineKeyboardButton(text="How to play", callback_data="how_to_play"),
            ],
        ],
    )

    await message.answer("Welcome!", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "how_to_play")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, about)


@dp.callback_query(lambda c: c.data == "register")
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "hm")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
