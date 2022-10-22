from flask_app import app
import config

if __name__ == "__main__":
    app.run(host=config.FlaskSettings.host,
            port=config.FlaskSettings.port,
            debug=True,
            threaded=True,
            use_reloader=False)
