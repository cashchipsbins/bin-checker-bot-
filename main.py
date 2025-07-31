import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN", "8291001795:AAFT1huvEo36yhuM8AYVVCkVR-aB5DT-0lE")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("👋 Отправь мне BIN (6-8 цифр), и я покажу информацию о карте.")

@dp.message_handler(lambda message: message.text.isdigit() and 6 <= len(message.text) <= 8)
async def check_bin(message: types.Message):
    bin_number = message.text
    url = f"https://lookup.binlist.net/{{bin_number}}"
    headers = {{"Accept-Version": "3"}}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        country = data.get("country", {{}}).get("name", "N/A")
        bank = data.get("bank", {{}}).get("name", "N/A")
        brand = data.get("scheme", "N/A").upper()
        card_type = data.get("type", "N/A").upper()
        level = data.get("brand", "N/A").upper()
        reply = f"🏦 Bank: {{bank}}\n🌍 Country: {{country}}\n💳 Brand: {{brand}}\n🧾 Type: {{card_type}}\n📶 Level: {{level}}"
    else:
        reply = "❌ BIN не найден или ошибка при запросе."
    await message.reply(reply)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
