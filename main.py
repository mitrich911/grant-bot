import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import telebot

from parsers import (
    get_rosmolodezh, get_fasie_news, get_skolkovo,
    get_generations, get_president_grants, get_moscow_mbm
)

# Загружаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def job():
    all_posts = []
    all_posts += get_rosmolodezh()
    all_posts += get_fasie_news()
    all_posts += get_skolkovo()
    all_posts += get_generations()
    all_posts += get_president_grants()
    all_posts += get_moscow_mbm()

    for post in all_posts:
        text = f"📢 {post['title']}\n\nИсточник: {post['source']}\n"
        if post["deadline"]:
            text += f"⏰ Дедлайн: {post['deadline']}\n"
        text += f"Подробнее: {post['link']}"
        try:
            bot.send_message(CHANNEL_ID, text, disable_web_page_preview=False)
        except Exception as e:
            logging.error(f"Ошибка при отправке: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scheduler = BlockingScheduler()
    scheduler.add_job(job, "interval", hours=1)
    logging.info("Бот запущен")
    job()  # Первая выгрузка сразу
    scheduler.start()