__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from models import BaseModel
from util.commons import Column

class Product(BaseModel):
    __tablename__ = 'products'

    id = Column(name='id')
    brand = Column(name='brand')
    sku = Column(name='sku')
    title = Column(name='title')
    description = Column(name='description')
    category = Column(name='category')
    prod_type = Column(name='prod_type')
    mrp = Column(name='mrp')
    available_price = Column(name='available_price')
    discount_percentage = Column(name='discount_percentage')
    discount_range = Column(name='discount_range')

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'title': self.title,
            'description': self.description,
            'sku': self.sku,
            'prod_type': self.prod_type,
            'mrp': self.mrp,
            'available_price': self.available_price,
            'discount_percentage': self.discount_percentage,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
