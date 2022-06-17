import logging
import requests

from ini_service import load_config

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