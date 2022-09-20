import logging
import time
import threading
import os

from helpers import datetime_dict
from services.check_metrics import Checker
from services.backup import Backup


class ServicesTask:
    @staticmethod
    def main_loop():
        """
        Главный цикл проверки
        """
        while True:
            try:
                now_dict = datetime_dict()
                Checker.run(now_dict=now_dict)
                Backup.run(now_dict=now_dict)
            except Exception as _ex:
                logging.exception(f'Unrecognized exception {_ex}')
            time.sleep(1)

    @staticmethod
    def run():
        # хинт, что бы процессы не двоились
        if 'WERKZEUG_RUN_MAIN' not in os.environ:
            mlt = threading.Thread(target=ServicesTask.main_loop)
            mlt.start()
