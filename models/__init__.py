__author__ = "Suyash Soni"
__email__ = "suyash.soni@srijan.net"
__copyright__ = "Copyright 2018, Srijan Technologies"

from .base import BaseModel, Column
from .product import Product
from .category import Category

__all__ = ['BaseModel', 'Column', 'Product', 'Category']

# Products
# id, name.....cat_id

# Category
# id, name, parent

# Product type
# id, name
