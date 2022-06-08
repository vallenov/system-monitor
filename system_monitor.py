import logging
import threading
import os

from flask_app import app
from check_functions import Checker


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # хинт, что бы процессы не двоились
    Checker.run()
    app.run(host='0.0.0.0', port=5112, debug=True, threaded=True)

