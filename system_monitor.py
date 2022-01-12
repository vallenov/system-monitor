import requests
import configparser
import logging
import time

from monitor_classes import Monitor


def load_config():
    config = configparser.ConfigParser()
    config.read('system_monitor.ini', encoding='utf-8')
    return config


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    conf = load_config()
    while True:
        try:
            conf = load_config()

            MAX_TEMP = int(conf.get('MAX_VALUES', 'max_temp'))

            name, temp = Monitor.get_temperature()
            if temp >= MAX_TEMP and Monitor.block_message.get('temperature', False) is False:
                data = dict()
                data['to'] = conf.get('CONTACT', 'telegram_name')
                data['text'] = f'Температура {name} выше {MAX_TEMP}°C'
                requests.post(conf.get('URL', 'message_server_address'), data=data, headers={'Connection': 'close'})
                Monitor.block_message['temperature'] = True
        except Exception as _ex:
            logging.exception(f'Unrecognize exception {_ex}')

        time.sleep(int(conf.get('SETTINGS', 'sleep_time')))

