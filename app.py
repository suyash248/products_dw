__author__ = "Suyash Soni"
__email__ = "suyash.soni.248@gmail.com"

import thirdparty # Don't remove this import, it's responsible for creating DB connection
import json, logging
from flask_restful import Api
from settings import app, config
from util.logger import Logger
from routes import register_urls

app.url_map.strict_slashes = False
api = Api(app)

def init_logger():
    log_level = getattr(logging, config['LOGGING']['LEVEL'], logging.INFO)

    Logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s -> %(name)s] at %(asctime)s in %(filename)s: %(lineno)s - %(message)s'))

    Logger.addHandler(stream_handler)

    app.logger.handlers = Logger.handlers
    app.logger.setLevel(log_level)

    Logger.info('Initializing logger...')

# Registering routes.
register_urls(api)

@app.route("/")
@app.route("/api/v1/")
def index():
    return json.dumps({"message": "Welcome to Products inventory."})

init_logger()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

