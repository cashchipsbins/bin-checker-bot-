
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, работаю на Render.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
