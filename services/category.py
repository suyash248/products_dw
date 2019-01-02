__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from services.base import BaseService
from models import Product, Category
from psycopg2.extras import RealDictCursor
from services.ecom_dao import EcomDao
from util.injector import inject
from uuid import uuid4

class CategoryService(BaseService):

    ecom_dao: EcomDao = inject(EcomDao)

    def get_category(self, id, fetch_hierarchy=False):
        cat = self.ecom_dao.get_by_id(Category, id)
        if fetch_hierarchy: return cat

        if cat:
            _cat = cat
            while _cat['parent']:
                _cat['parent'] = self.ecom_dao.get_by_id(Category, _cat['parent'])
                _cat = _cat['parent']
            return cat


    def get_all_products(self):
        return self.ecom_dao.get_all(Product)

    def update_product(self, id, **params):
        self.ecom_dao.update_by_id(Product, id, **params)

    def count_products(self, criteria=[]):

        fields = ', '.join([Product.__tablename__ + '.' + col + ' as prod_' + col for col in Product.columns()]) \
                 + ',' + ','.join([Category.__tablename__ + '.' + col + ' as cat_' + col for col in Category.columns()])
        whereclause_attrs = []
        whereclause_kv = {}
        whereclause = ''

        if len(criteria) > 0:
            for criterion in criteria:
                whereclause_attrs.append("{field_name}{operator}%%({field_name})s".format(**criterion))
                whereclause_kv[criterion['field_name']] = criterion['field_value']

            whereclause = " WHERE " + "AND ".join(whereclause_attrs)

        query = """
                SELECT COUNT({prod}.id) FROM {prod} LEFT JOIN {cat} ON {prod}.category = {cat}.id
                {whereclause}
                """.format(fields=fields, prod=Product.__tablename__, cat=Category.__tablename__,
                                   whereclause=whereclause)

        print(query)
        with self.pg_con:
            with self.pg_con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, whereclause_kv)
                return cur.fetchone().get('count', 0)

    def paginate_products(self, criteria=[], page=1, per_page=10):
        """
        Fetches products' list.
        :param page: Current page, defaults to 1
        :param per_page: Number of records per page, defaults to 10
        :return: List of products
        """
        limit = per_page
        offset = limit * (page-1)

        fields = ', '.join([Product.__tablename__ + '.'+ col + ' as prod_' + col for col in Product.columns()]) \
                 + ',' + ','.join([Category.__tablename__ + '.'+ col + ' as cat_' + col for col in Category.columns()])
        whereclause_attrs = []
        whereclause_kv = {}
        whereclause = ''

        if len(criteria) > 0:
            for criterion in criteria:
                whereclause_attrs.append("{field_name}{operator}%%({field_name})s".format(**criterion))
                whereclause_kv[criterion['field_name']] = criterion['field_value']

            whereclause = " WHERE " + "AND ".join(whereclause_attrs)

        query = """
                SELECT {fields} FROM {prod} LEFT JOIN {cat} ON {prod}.category = {cat}.id
                {whereclause} LIMIT {limit} OFFSET {offset}
                """.format(fields=fields, prod=Product.__tablename__, cat=Category.__tablename__,
                           whereclause=whereclause, limit=limit, offset=offset)

        print(query)
        with self.pg_con:
            with self.pg_con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, whereclause_kv)
                return cur.fetchall()

    def add_product(self, title, description, sku, brand, category, prod_type, mrp):
        """
        Adds a product.
        """
        cols = Product.columns()
        fields = ', '.join(cols)
        values = ', '.join(['%%(%s)s' % c for c in cols])

        q = "INSERT INTO {table} ({fields}) VALUES ({values})".format(
                    table=Product.__tablename__, fields=fields, values=values)
        params = dict(id=str(uuid4()), title=title, description=description, sku=sku, brand=brand, category=category,
                      prod_type=prod_type, mrp=mrp)
        print(q)
        with self.pg_con:
            with self.pg_con.cursor() as curs:
                curs.execute(q, params)
