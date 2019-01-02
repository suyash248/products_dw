__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from abc import ABC, abstractmethod
from util.commons import Column
from uuid import uuid4

class BaseModel(ABC):

    __tablename__ = ''

    created_at = Column(name='created_at')
    updated_at = Column(name='updated_at')

    @classmethod
    def fields(cls):
        return list(filter(lambda f: isinstance(getattr(cls, f, None), Column), dir(cls)))

    @classmethod
    def columns(cls, sep='.', prefix='', suffix=''):
        cols = filter(lambda f: isinstance(getattr(cls, f, None), Column), dir(cls))
        if prefix or suffix:
            prefix = prefix + sep if prefix else ''
            suffix = sep + suffix if suffix else ''
            cols =map(lambda c: prefix + c + suffix, cols)
        cols =  tuple(cols)
        return cols

    @classmethod
    def yield_rows(cls, pg_con, page_size=1000, query=None):
        cur_name = 'cur_{}_{}'.format(cls.__tablename__, str(uuid4()))
        with pg_con:
            with pg_con.cursor(name=cur_name) as cursor:
                cursor.itersize = page_size
                fields = ', '.join(cls.columns())
                query = query or "SELECT {fields} from {table}".format(fields=fields, table=cls.__tablename__)
                cursor.execute(query)
                yield from cursor
                # for row in cursor:
                     # process row

    @classmethod
    def build(cls, row_dict):
        model_obj = cls()
        for f, v in row_dict.items():
            if getattr(model_obj, f, None):
                setattr(model_obj, f, v)
        return model_obj

    def to_dict(self):
        pass