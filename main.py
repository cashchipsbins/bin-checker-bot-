from aiogram import Bot, Dispatcher, types, executor
import requests

API_TOKEN = "8291001795:AAFT1huvEo36yhuM8AYVVCkVR-aB5DT-0lE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Отправь BIN, и я скажу, к какому банку он относится.")

@dp.message_handler()
async def check_bin(message: types.Message):
    bin_number = message.text.strip()
    if not bin_number.isdigit() or len(bin_number) < 6:
        await message.reply("Пожалуйста, введи корректный BIN (минимум 6 цифр).")
        return

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Неизвестно")
            scheme = data.get("scheme", "Неизвестно")
            brand = data.get("brand", "Неизвестно")
            country = data.get("country", {}).get("name", "Неизвестно")
            await message.reply(
                f"Банк: {bank}
Схема: {scheme}
Бренд: {brand}
Страна: {country}"
            )
        else:
            await message.reply("BIN не найден.")
    except Exception as e:
        await message.reply("Ошибка при запросе.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
