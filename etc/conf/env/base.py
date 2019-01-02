__author__ = "Suyash Soni"
__email__ = "suyash.soni.248@gmail.com"

import os

class BaseConfig(object):
    URLS_PREFIX = "/api/v1"
    PG_DB_CONFIG = {
        'URI_CONFIG': {
            'dbname': os.environ['PG_DB_NAME'],
            'host': os.environ['PG_DB_HOST'],
            'user': os.environ['PG_DB_USERNAME'],
            'password': os.environ['PG_DB_PASSWORD'],
            'port': os.environ['PG_DB_PORT']
        },
        'CONNECTION_POOL_SIZE': os.environ.get('CONNECTION_POOL_SIZE', 5)
    }
    CORS_ORIGIN_REGEX_WHITELIST = ['*']
    LOGGING = {
        "LEVEL": os.environ.get('LOG_LEVEL', 'INFO'),

    }
    STATIC_FILES_DIR = 'static'
    FIELDS_SEPARATOR = '|'