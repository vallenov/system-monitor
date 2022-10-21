import logging

from flask_app import app
import config

if __name__ == "__main__":
    logging.basicConfig(filename='run.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.run(host=config.FlaskSettings.host,
            port=config.FlaskSettings.port,
            debug=True,
            threaded=True,
            use_reloader=False)
