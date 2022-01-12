import requests
import configparser

from monitor_classes import Monitor

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('system_monitor.ini', encoding='utf-8')

    MAX_TEMP = int(config.get('MAX_VALUES', 'max_temp'))

    if Monitor.get_temperature() > MAX_TEMP:
        data = dict()
        data['to'] = config.get('CONTACT', 'telegram_name')
        data['text'] = f'Температура малинки выше {MAX_TEMP}!'
        requests.post(config.get('URL', 'message_server_address'), data=data, headers={'Connection':'close'})
