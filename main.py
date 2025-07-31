import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = "8291001795:AAFT1huvEo36yhuM8AYVVCkVR-aB5DT-0lE"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def lookup_bin(bin_code):
    url = f"https://lookup.binlist.net/{bin_code}"
    headers = {"Accept-Version": "3"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "BIN не найден или ошибка при запросе."
    data = response.json()
    result = [
        f"Country: {data.get('country', {}).get('name', 'N/A')}",
        f"Bank: {data.get('bank', {}).get('name', 'N/A')}",
        f"Brand: {data.get('scheme', 'N/A').upper()}",
        f"Type: {data.get('type', 'N/A').upper()}",
        f"Level: {data.get('brand', 'N/A').upper()}",
    ]
    return "\n".join(result)

@dp.message_handler()
async def handle_message(message: types.Message):
    if not message.text.isdigit() or len(message.text) < 6:
        await message.reply("Пожалуйста, отправьте корректный BIN (6+ цифр).")
        return
    info = lookup_bin(message.text)
    await message.reply(info)

if __name__ == "__main__":
    executor.start_polling(dp)
