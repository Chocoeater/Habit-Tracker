
from django.conf import settings
import requests

# from telegram import Bot
# import asyncio

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

# Не работает почему-то, выдает TimeOut, разберусь потом.

# async def _async_send_message(telegram_id: str, message: str):
#     """Отправляет уведомление пользователю в Telegram."""
#     try:
#         async with Bot(token=TELEGRAM_BOT_TOKEN) as bot:
#             await bot.send_message(chat_id=telegram_id, text=message)
#     except Exception as e:
#         print(f"Ошибка при отправке сообщения в Telegram: {e}")
#
#
# def send_telegram_notification(telegram_id: str, message: str):
#     """Синхронная обертка для асинхронной отправки"""
#     return asyncio.run(_async_send_message(telegram_id, message))

def send_telegram_notification(telegram_id: str, message: str):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': telegram_id,
        'text': message,
    }
    requests.post(url, json=params)

