from settings import config
import psycopg2

def init_pg():
    con = psycopg2.connect(**config['PG_DB_CONFIG']['CON_PARAMS'])
    return con

config['pg_con'] = init_pg()