import sqlite3

class DatabaseIntegration:
  DATABASE = "estoque.db"

  def __init__(self, table):
    self.table = table
    self.db = self.DATABASE
    self.init_database()

  def init_database(self):
    conn = None
    try:
      conn = sqlite3.connect(self.DATABASE)
      print('Database conected successfully')
      cursor = conn.cursor()
      cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          category TEXT NOT NULL,
          quantity INTEGER NOT NULL,
          price REAL NOT NULL
        );
        """
      )
      conn.commit()
      conn.close()
    except sqlite3.Error as ex:
      print(f"Erro ao inicializar o banco de dados: {ex}")
      conn.close()
    finally:
      if conn:
        conn.close()
  
  def insert(self, document):
    conn = None
    try:
      keys = len(document)
      columns = list(document.keys())
      values = list(document.values())
      query = f"""
        INSERT INTO {self.table} ({", ".join(columns)}) 
        VALUES ({", ".join(['?'] * keys)})
      """
      conn = sqlite3.connect(self.db)
      cursor = conn.cursor()
      cursor.execute(query, values)
      conn.commit()
      print(f"Registro inserido com sucesso!\n {document}")
    except sqlite3.Error as ex:
      print(f"Erro ao inserir o documento {ex}")
    finally:
      if conn:
        conn.close()
    return document
  
  def find(self, where=None):
    conn = None
    documents = []
    try:
      conn = sqlite3.connect(self.db)
      cursor = conn.cursor()
    
      if where is None or not where:
        query = f"SELECT * FROM {self.table};"
        cursor.execute(query)
      else:
        columns = " AND ".join([f"{key} = ?" for key in where.keys()])
        query = f"SELECT * FROM {self.table} WHERE {columns}"
        values = list(where.values())
        cursor.execute(query, values)
      
      documents = cursor.fetchall()
    except sqlite3.Error as ex:
      print(f'Erro ao buscar os documentos: {ex}')
    finally:
      if conn:
        conn.close()
    return documents
  
  def findOne(self, id):
    conn = None
    try:
      query = f"""
        SELECT * FROM {self.table} WHERE id = ?
      """
      conn = sqlite3.connect(self.db)
      cursor = conn.cursor()
      cursor.execute(query, (id,))
      document = cursor.fetchone()
      conn.close()
      return document
    except sqlite3.Error as ex:
      print(f"Erro ao buscar o documento: {ex}")
    finally:
      if conn:
        conn.close()

  
  def update(self, id, document):
    try:
      conn = sqlite3.connect(self.db)
      cursor = conn.cursor()
      columns = ", ".join([f"{key} = ?" for key in document.keys()])
      sql = f"UPDATE {self.table} SET {columns} WHERE id = ?"
      values = list(document.values()) + [id]
      cursor.execute(sql, values)
      conn.commit()
      conn.close()
    except sqlite3.Error as ex:
      print(f'Erro ao tentar atualizar o registro: {ex}')
    finally:
      if conn:
        conn.close()
    return document
  
  def delete(self, id):
    conn = None
    try:
      document = self.findOne(id)
      query = f"DELETE FROM {self.table} WHERE id = ?"
      if document:
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()
        conn.close()
        return True
      else:
        raise ValueError(f"O registro com ID {id} não foi encontrado no sistema.")
    except (sqlite3.Error, ValueError) as ex:
      print(f'Erro ao tentar excluir o registro {ex}')
      return False
    finally:
      if conn:
        conn.close()