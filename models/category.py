__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from models import BaseModel
from util.commons import Column

class Category(BaseModel):
    __tablename__ = 'categories'

    id = Column(name='id')
    name = Column(name='name')
    parent = Column(name='parent')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent': self.parent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
