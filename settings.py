__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import os
from flask import Flask

__basedir__ = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Ideally, there will be one config class per environment(dev, qa, uat, prod)
class __Config__(object):
    URLS_PREFIX = "/api/v1"
    PG_DB_CONFIG = {
        'CON_PARAMS': {
            'dbname': os.environ['PG_DB_NAME'],
            'host': os.environ['PG_DB_HOST'],
            'user': os.environ['PG_DB_USER'],
            'password': os.environ['PG_DB_PASSWORD'],
            'port': os.environ.get('PG_DB_PORT', 5432)
        },
        'CONNECTION_POOL_SIZE': os.environ.get('CONNECTION_POOL_SIZE', 5)
    }
    CORS_ORIGIN_REGEX_WHITELIST = ['*']
    LOGGING = {
        "LEVEL": os.environ.get('LOG_LEVEL', 'INFO'),

    }
    STATIC_FILES_DIR = 'static'
    FIELDS_SEPARATOR = '|'

app.config.from_object(__Config__)
config = app.config
config['APPLICATION_ROOT'] = __basedir__

__all__ = ["config", "app"]