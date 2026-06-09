from flask import Flask
from core.database import Database

app = Flask(__name__)
Database()
def init_server():
  try:
    print('Inicializando a API.')
    Database()
  except Exception as e:
    print(f'Erro ao inicializar a API: {e}')
