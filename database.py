# Importa o ORM(Object-Relational Mapping) para criar o banco de dados e manipular os dados utilizando a linguagem Python
from peewee import *

# Cria o banco de dados utilizando o SQLite
db = SqliteDatabase('passwords.db') # Gera um arquivo para armazenar o banco de dados

#Modelo base para todas as tabelar herdarem a mesma configuração de banco
class BaseModel(Model): # Model é a classe base do peewee para criar tabelas
    # Classe Meta para configurar a tabela
    class Meta:
        database = db # Define o banco de dados a ser utilizado

# Cria a tabela que irá armazenar as senhas
class Password(BaseModel): 
    title = CharField()
    password = TextField()

class Authentication(BaseModel):
    salt = BlobField()
    auth = CharField(max_length=255)
