__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from flask import request
from util.response import intercept, Response
from controllers.base import BaseController
from util.injector import inject
from services.product import ProductService
from util.constants.error_codes import HttpErrorCode
from util.error_handlers.exceptions import ExceptionBuilder, BadRequest

# => Build the following REST APIs using any Python API framework:
# - Enable filter on category, brand, source, subcategory
# - Search on title, sku
# - List out all the products
# - Update the product attributes like Brand, Category, Sub Category, Product Type

# => Update the discount value for each product. Discount = ((mrp -
# available_price)/(mrp)) * 100
# => Build an API to return count of products in each of the following discount buckets.
#  0%, 0-10%, 10-30%, 30-50%, >50%
#  *Bonus points if it’s optimized for speed

class ProductList(BaseController):
    product_service: ProductService = inject(ProductService)

    @intercept()
    def post(self, *args, **kwargs):
        """Adds a new document to repo"""

        data = request.get_json(force=True)

        brand = data.get('brand', '')
        title = data.get('title', '')
        description = data.get('description', '')
        sku = data.get('sku', '')
        category = data.get('category', -1)
        prod_type = data.get('prod_type', -1)
        mrp = data.get('mrp', -1)
        available_price = data.get('available_price', -1)
        self.product_service.add_product(title, description, sku, brand, category, prod_type, mrp, available_price)

        return Response(status_code=201, message='Product added successfully!')

    @intercept()
    def get(self):
        """
        Fetches all the documents(paginated).
        :return:
        """
        res = self.product_service.paginate_products(page=int(request.args.get("page", 1)),
                                    per_page=int(request.args.get("per_page", 10)))
        return Response(data=res)

class Product(BaseController):
    product_service: ProductService = inject(ProductService)

    @intercept()
    def put(self, product_id, *args, **kwargs):
        """Adds a new document to repo"""

        data = request.get_json(force=True)
        self.product_service.update_product(product_id, **data)
        return Response(status_code=200, message='Product updated successfully!')

    @intercept()
    def get(self, product_id):
        """
        Fetches all the documents(paginated).
        :return:
        """
        res = self.product_service.get_product(product_id)
        return Response(data=res)


class ProductFilter(BaseController):
    product_service: ProductService = inject(ProductService)

    @intercept()
    def post(self, *args, **kwargs):
        """Adds a new document to repo"""

        data = request.get_json(force=True)

        filter_by = data.get('filter_by', [])
        order_by = data.get('order_by', [])
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        res = self.product_service.paginate_products(filter_by=filter_by, order_by=order_by,
                                                     page=page, per_page=per_page)
        return Response(data=res)

class ProductsDiscount(BaseController):
    product_service: ProductService = inject(ProductService)

    @intercept()
    def get(self, *args, **kwargs):
        res = self.product_service.count_by_discount_range()
        return Response(data=res)