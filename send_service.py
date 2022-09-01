import logging
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from monitor import Monitor
import config

MAX_TRY = 15


def send_message(data: dict):
    """
    Отправка сообщения админу
    """
    current_try = 0
    while current_try < MAX_TRY:
        current_try += 1
        try:
            requests.post(config.Url.message_server_address + 'telegram',
                          data=data,
                          headers={'Connection': 'close'})
        except Exception as exc:
            logging.exception(exc)
        else:
            logging.info('Send successful')
            return
    logging.error('Max try exceeded')


def send_confirmation_message():
    bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✅ Allow/Подтвердить", callback_data="allow_connection"))
    bot.send_message(config.TELEGRAM_CHAT_ID,
                     f'Попытка нового подключения к {Monitor.get_name_of_machine()}',
                     reply_markup=markup)

