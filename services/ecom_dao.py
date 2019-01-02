__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from util.logger import Logger
from util.constants.error_codes import HttpErrorCode
from util.error_handlers.exceptions import ExceptionBuilder, BadRequest
from services.base import BaseService
from psycopg2.extras import RealDictCursor

class EcomDao(BaseService):

    def get_by_id(self, model_cls, id):
        fields = ', '.join(model_cls.columns())
        q = "SELECT {fields} from {table} WHERE id=%(id)s".format(fields=fields, table=model_cls.__tablename__)
        with self.pg_con:
            with self.pg_con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(q, {'id': id})
                return model_cls.build(cur.fetchone()).to_dict()

    def get_all(self, model_cls):
        fields = ', '.join(model_cls.columns())
        q = "SELECT {fields} from {table}".format(fields=fields, table=model_cls.__tablename__)
        with self.pg_con:
            with self.pg_con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(q)
                return [model_cls.build(rec).to_dict() for rec in cur.fetchall()]

    def update_by_id(self, model_cls, id, **params):
        rec = self.get_by_id(model_cls, id)
        if not rec:
            ExceptionBuilder(BadRequest).error(HttpErrorCode.NOT_FOUND, id,
                    message='No such {} found!'.format(model_cls.__tablename__)).throw()
        # "UPDATE table_name SET col1=(%s), col2=(%s) WHERE ref_column_id_value = (%s)"
        update_cols = ','.join(['{col}=%({col})s'.format(col=uc) for uc in params.keys()])
        q = """
            UPDATE {table} SET {update_cols} WHERE id=%(id)s
        """.format(table=model_cls.__tablename__, update_cols=update_cols)
        params['id'] = id
        Logger.info(q)
        with self.pg_con:
            with self.pg_con.cursor() as curs:
                curs.execute(q, params)