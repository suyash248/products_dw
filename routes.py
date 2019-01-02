__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from controllers import product

def add_prefix(uri):
    return "{}{}".format('/api/v1', uri)

def register_urls(api):
    """
    Maps all the endpoints with controllers.
    """
    api.add_resource(product.ProductList, add_prefix('/products'))
    api.add_resource(product.ProductFilter, add_prefix('/products/filter'))
    api.add_resource(product.Product, add_prefix('/products/<product_id>'))
    api.add_resource(product.ProductsDiscount, add_prefix('/products/discounts'))