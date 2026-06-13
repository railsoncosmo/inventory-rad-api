from core.database import DatabaseIntegration
from helpers.helper_class import HelperClass


class CoreService:
  def __init__(self, table, entity_class):
    self.db = DatabaseIntegration(table)
    self.entity_class = entity_class

  def insert(self, document):
    if document is None:
      return None
    data = HelperClass._parse_document(document)
    entity = self.entity_class(data)
    return self.db.insert(entity.to_dict())

  def find(self, where=None):
    documents = self.db.find(where)
    if documents is None:
      return []
    return [HelperClass._row_to_dict(row) for row in documents]

  def findOne(self, id):
    document = self.db.findOne(str(id))
    if document is None:
      raise ValueError('Documento não encontrado.')
    return HelperClass._row_to_dict(document)

  def update(self, id, document):
    existing = self.db.findOne(str(id))
    if existing is None:
      raise ValueError('Documento não encontrado.')
    if document is None:
      raise ValueError('Documento de atualização não informado.')
    data = HelperClass._parse_document(document)
    entity = self.entity_class(data)
    return self.db.update(id, entity.to_dict())

  def delete(self, id):
    existing = self.db.findOne(str(id))
    if existing is None:
      raise ValueError('Documento não encontrado.')
    return self.db.delete(id)
