
class Product:
  def __init__(self, name, category=None, quantity=None, price=None):
    if isinstance(name, dict):
      data = name
      name = data['name']
      category = data['category']
      quantity = data['quantity']
      price = data['price']
    self.name = name
    self.category = category
    self.quantity = quantity
    self.price = price

  def to_dict(self):
    return {
      'name': self.name,
      'category': self.category,
      'quantity': self.quantity,
      'price': self.price,
    }
