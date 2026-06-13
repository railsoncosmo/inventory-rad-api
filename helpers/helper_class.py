import json

class HelperClass:
  @staticmethod
  def _parse_document(document):
    if isinstance(document, str):
      return json.loads(document)
    if isinstance(document, dict):
      return document
    raise ValueError('Documento inválido.')

  @staticmethod
  def get_columns(row):
    if row is None:
      return []
    if isinstance(row, dict):
      return list(row.keys())
    return list(row.keys())

  @staticmethod
  def _row_to_dict(row):
    if row is None:
      return None
    return dict(zip(HelperClass.get_columns(row), row))
