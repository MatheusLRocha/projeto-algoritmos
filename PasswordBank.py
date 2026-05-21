from database import Password, db # Importa a classe Password e o banco de dados do arquivo database.py

class PasswordRepository:
    def __init__(self):
        db.connect() # Conecta ao banco de dados
        db.create_tables([Password]) # Cria a tabela de senhas no banco de dados, caso ela ainda não exista

    # CRUD(Create, Read, Update, Delete) para manipular os dados do banco de dados utilizando a classe Password

    def add(self, title, password):
        # Cria um novo registro de senha no banco de dados utilizando a classe Password
        Password.create(title=title, password=password) 

    def list(self):
        # Retorna todas as senhas armazenadas no banco de dados
        return Password.select()
    
    def update(self, id, new_password):
        senha = Password.get(Password.id == id)
        senha.password = new_password
        senha.save()

    def delete(self, title):
        senha = Password.get(Password.title == title)
        senha.delete_instance()

    def new_register(self):
        Password.delete().execute()

    
        


        
        



