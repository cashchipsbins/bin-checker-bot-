import os
import logging
import time
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes, MessageHandler, filters
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

logger = logging.getLogger(__name__)

# Ограничение по времени (анти-спам)
user_last_request = {}

# Статистика
total_requests = 0

def get_bin_info(bin_number: str) -> str:
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code != 200:
            return "❌ Не удалось найти информацию. Убедитесь, что введён правильный BIN (6-8 цифр)."

        data = response.json()
        country = data.get("country", {}).get("name", "Неизвестно")
        bank = data.get("bank", {}).get("name", "Неизвестно")
        brand = data.get("scheme", "Неизвестно").upper()
        card_type = data.get("type", "Неизвестно").upper()
        level = data.get("brand", "Неизвестно").upper()

        return (
            f"✅ Информация о BIN {bin_number}:
"
            f"🏦 Bank: {bank}
"
            f"🌍 Country: {country}
"
            f"💳 Brand: {brand}
"
            f"📄 Type: {card_type}
"
            f"⭐ Level: {level}"
        )
    except Exception as e:
        logger.error(f"Ошибка при запросе BIN: {e}")
        return "⚠️ Произошла ошибка при получении данных."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне BIN (6-8 цифр), и я покажу информацию о карте.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 Всего запросов обработано: {total_requests}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_requests

    user_id = update.message.from_user.id
    now = time.time()
    if user_id in user_last_request and now - user_last_request[user_id] < 5:
        await update.message.reply_text("⏱ Подожди 5 секунд перед следующим запросом.")
        return
    user_last_request[user_id] = now

    bin_number = update.message.text.strip()
    if not bin_number.isdigit() or len(bin_number) < 6:
        await update.message.reply_text("❌ Пожалуйста, введите корректный BIN (6-8 цифр).")
        return

    logger.info(f"Пользователь {user_id} запросил BIN: {bin_number}")
    total_requests += 1
    result = get_bin_info(bin_number)
    await update.message.reply_text(result)

def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("8291001795:AAEHB171u_CQ5fXG0X5QDXpN8-wEY2AKbtY")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
