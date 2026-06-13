from core.database import DatabaseIntegration
import json
from entities.product import Product

db = DatabaseIntegration("products")
class CoreService:

  def insert(document):
    if document is None:
      return
    
    data = json.loads(document)
    product = Product(data)
    db.insert(product.__dict__)
    return True
  
  def find(where=None):
    return True
  
  def findOne(id):
    try:
      document = db.findOne(str(id))
      if document is None:
        return ValueError('Documento não encontrado.')
      
      return document
    except Exception as ex:
      print(f'Erro ao buscar documento solicitado: {ex}')
  
  def update(id):
    return True
  
  def delete(id):
    return True