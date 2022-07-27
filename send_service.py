import logging
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from ini_service import load_config
from monitor import Monitor

MAX_TRY = 15


def send_message(data: dict):
    """
    Отправка сообщения админу
    """
    current_try = 0
    conf = load_config()
    while current_try < MAX_TRY:
        current_try += 1
        try:
            requests.post(conf.get('URL', 'message_server_address') + 'telegram',
                          data=data,
                          headers={'Connection': 'close'})
        except Exception as exc:
            logging.exception(exc)
        else:
            logging.info('Send successful')
            return
    logging.error('Max try exceeded')


def send_confirmation_message():
    conf = load_config()
    bot = telebot.TeleBot(conf.get('TELEBOT', 'token'))
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✅ Allow/Подтвердить", callback_data="allow_connection"))
    bot.send_message(conf.get('TELEBOT', 'root_id'),
                     f'Попытка нового подключения к {Monitor.get_name_of_machine()}',
                     reply_markup=markup)

