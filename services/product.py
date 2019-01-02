__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from util.logger import Logger
from services.base import BaseService
from models import Product, Category
from psycopg2.extras import RealDictCursor
from services.ecom_dao import EcomDao
from util.injector import inject
from uuid import uuid4
from services.discount import DiscountService
from util.query.select import Query
from datetime import datetime

class ProductService(BaseService):

    ecom_dao: EcomDao = inject(EcomDao)
    discount_service: DiscountService = inject(DiscountService)

    def get_product(self, id):
        return self.ecom_dao.get_by_id(Product, id)

    def get_all_products(self):
        return self.ecom_dao.get_all(Product)

    def update_product(self, id, **params):
        if Product.mrp.name in params or Product.available_price.name in params:
            old_prod = self.get_product(id)
            mrp = params.get('mrp', old_prod['mrp'])
            available_price = params.get('available_price', old_prod['available_price'])

            params['discount_percentage'] = self.discount_service.calculate_discount(mrp, available_price)
            params['discount_range'] = self.discount_service.discount_range(params['discount_percentage'])

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

    def paginate_products(self, filter_by={}, order_by=(), page=1, per_page=10):
        """
        Fetches products' list.
        :param page: Current page, defaults to 1
        :param per_page: Number of records per page, defaults to 10
        :return: List of products
        """

        def mapper(row_dict):
            row_dict['product_created_at'] = row_dict['product_created_at'].isoformat() if row_dict.get('product_created_at', None) else None
            row_dict['product_updated_at'] = row_dict['product_updated_at'].isoformat() if row_dict.get('product_updated_at', None) else None
            return row_dict

        selectables = (Product.id.label(Product.__tablename__, 'product_id'),
                       Product.title, Product.brand, Product.description, Product.sku, Product.category,
                        Product.created_at.label(Product.__tablename__, 'product_created_at'),
                        Product.updated_at.label(Product.__tablename__, 'product_updated_at'),
                        Category.name.label(Category.__tablename__, 'category_name'),
                        Category.parent.label(Category.__tablename__, 'super_category')
                       )
        results = Query.select(*selectables)\
                .from_table(Product)\
                .leftjoin(Category, Product.category, Category.id)\
                .where(and_criteria=filter_by.get('and', []), or_criteria=filter_by.get('or', []))\
                .slice(page=page, per_page=per_page).order_by(*order_by).build().exec(self.pg_con, mapper=mapper)
        return results

    def add_product(self, title, description, sku, brand, category, prod_type, mrp, available_price):
        """
        Adds a product.
        """
        cols = Product.columns()
        fields = ', '.join(cols)
        values = ', '.join(['%%(%s)s' % c for c in cols])

        discount_percentage = self.discount_service.calculate_discount(mrp, available_price)
        discount_range = self.discount_service.discount_range(discount_percentage)

        q = "INSERT INTO {table} ({fields}) VALUES ({values})".format(
                    table=Product.__tablename__, fields=fields, values=values)
        params = dict(id=str(uuid4()), title=title, description=description, sku=sku, brand=brand, category=category,
                      prod_type=prod_type, mrp=mrp, available_price=available_price,
                      discount_percentage=discount_percentage, discount_range=discount_range,
                      created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        Logger.info(q)
        with self.pg_con:
            with self.pg_con.cursor() as curs:
                curs.execute(q, params)

    def count_by_discount_range(self):
        query = "SELECT {discount_range}, COUNT({discount_range}) FROM {table} GROUP BY {discount_range}".format(
            table=Product.__tablename__, discount_range=Product.discount_range.name
        )
        with self.pg_con:
            with self.pg_con.cursor() as curs:
                curs.execute(query)
                return {tp[0]: tp[1] for tp in curs.fetchall()}