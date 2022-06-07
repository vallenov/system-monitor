import logging
import time
import threading

from ini_service import load_config
from check_functions import (
    check_ip,
    check_temperature,
    check_ssh_connections,
    check_used_space,
)


def check_loop():
    i = 0
    sec = 1
    minute = sec * 60

    while True:
        i = 0 if i > 600 else i
        try:
            if i and not i % 5 * sec:
                check_ip()
                check_ssh_connections()
            if i and not i % minute:
                check_temperature()
            if i and not i % 5 * minute:
                check_used_space()
        except Exception as _ex:
            logging.exception(f'Unrecognized exception {_ex}')
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    cl = threading.Thread(target=check_loop)
    cl.start()

