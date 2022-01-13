import requests
import configparser
import logging
import time

from monitor_classes import Monitor


def load_config():
    config = configparser.ConfigParser()
    config.read('system_monitor.ini', encoding='utf-8')
    return config


conf = load_config()


def send_message(data: dict):
    requests.post(conf.get('URL', 'message_server_address'), data=data, headers={'Connection': 'close'})


def check_temperature():

    max_temp = int(conf.get('MAX_VALUES', 'max_temp'))

    temp = Monitor.get_temperature()
    if temp >= max_temp and Monitor.block_message.get('temperature', False) is False:
        data = dict()
        data['to'] = conf.get('CONTACT', 'telegram_name')
        name = Monitor.get_name_of_machine()
        data['text'] = f'Температура {name} выше {max_temp}°C'
        send_message(data)
        logging.info('Send successful')
        Monitor.block_message['temperature'] = True
    elif temp < max_temp:
        Monitor.block_message['temperature'] = False


def check_used_space():
    max_used_space = int(conf.get('MAX_VALUES', 'max_used_space'))
    used_space = Monitor.get_used_space()
    name = Monitor.get_name_of_machine()
    for key, value in used_space.items():
        if value > max_used_space and Monitor.block_message.get(f'used_space{key}', False) is False:
            data = dict()
            data['to'] = conf.get('CONTACT', 'telegram_name')
            data['text'] = f'Свободное место в "{key}" на сервере {name} заканчивается. Осталось {100 - value}%'
            send_message(data)
            Monitor.block_message[f'used_spase{key}'] = True
        else:
            Monitor.block_message[f'used_spase{key}'] = False


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        try:
            conf = load_config()
            check_temperature()
            check_used_space()
        except Exception as _ex:
            logging.exception(f'Unrecognized exception {_ex}')

        time.sleep(int(conf.get('SETTINGS', 'sleep_time')))

