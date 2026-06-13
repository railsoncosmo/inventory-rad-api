from core.service import CoreService
from entities.product_class import Product


class ProductService(CoreService):
  def __init__(self):
    super().__init__('products', Product)
