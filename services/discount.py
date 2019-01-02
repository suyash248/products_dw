__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from services.base import BaseService

class DiscountService(BaseService):

    def calculate_discount(self, mrp, available_price):
        discount_percentage = ((mrp - available_price)/mrp) * 100
        discount_percentage = round(discount_percentage, 2)
        return discount_percentage

    def discount_range(self, discount_percentage):
        # 0%, 0-10%, 10-30%, 30-50%, >50%
        disc_range = '{from}_{to}'
        if discount_percentage <= 0:
            return '0%'
        elif 0 < discount_percentage < 10:
            return '0-10%'
        elif 10 <= discount_percentage < 30:
            return '10-30%'
        elif 30 <= discount_percentage < 50:
            return '30-50%'
        elif discount_percentage >= 50:
            return '>50'