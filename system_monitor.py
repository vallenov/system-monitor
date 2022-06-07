import logging
import threading
import os

from flask_app import app
from check_functions import check_loop


if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # хинт, что бы процессы не двоились
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        cl = threading.Thread(target=check_loop)
        cl.start()
    app.run(host='0.0.0.0', port=5112, debug=True, threaded=True)

