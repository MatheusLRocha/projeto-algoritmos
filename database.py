# Importa o ORM(Object-Relational Mapping) para criar o banco de dados e manipular os dados utilizando a linguagem Python
from peewee import *

# Cria o banco de dados utilizando o SQLite
db = SqliteDatabase('passwords.db') # Gera um arquivo para armazenar o banco de dados

# Cria a tabela que irá armazenar as senhas
class Password(Model): # Model é a classe base do peewee para criar tabelas
    title = CharField()
    password = TextField()

    # Classe Meta para configurar a tabela
    class Meta:
        database = db # Define o banco de dados a ser utilizado