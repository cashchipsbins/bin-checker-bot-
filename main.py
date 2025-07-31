import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests

BOT_TOKEN = "8291001795:AAFT1huvEo36yhuM8AYVVCkVR-aB5DT-0lE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 Отправь мне BIN (первые 6 цифр карты), и я скажу информацию о нём.")

@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) in [6, 8])
async def check_bin(message: types.Message):
    bin_code = message.text.strip()
    response = requests.get(f"https://lookup.binlist.net/{bin_code}")
    if response.status_code == 200:
        data = response.json()
        country = data.get("country", {}).get("name", "Unknown")
        bank = data.get("bank", {}).get("name", "Unknown")
        brand = data.get("scheme", "Unknown").upper()
        type_ = data.get("type", "Unknown").upper()
        level = data.get("brand", "Unknown").upper()

        reply = f"""💳 BIN: {bin_code}
🌍 Country: {country}
🏦 Bank: {bank}
💳 Brand: {brand}
🧾 Type: {type_}
📶 Level: {level}"""
        await message.answer(reply)
    else:
        await message.answer("❌ Не удалось получить информацию. Проверь BIN.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
