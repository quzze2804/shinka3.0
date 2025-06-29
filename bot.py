import os
import telegram
from telegram.ext import Updater, CommandHandler
import schedule
import time
import threading

# Получите токен из переменной окружения для безопасности
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Ваш ID

bot = telegram.Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text("Добро пожаловать! Я буду напоминать о записях.")

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

# Расписание для напоминаний (например, каждые 30 минут с 8 до 17)
def schedule_notifications():
    for hour in range(8, 17):
        for minute in [0, 30]:
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(send_message, text="Пора записаться на шиномонтаж!")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Планируем уведомления
    schedule_notifications()
    thread = threading.Thread(target=run_schedule)
    thread.start()

    # Запускаем бота
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
