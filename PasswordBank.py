from database import Password, Authentication, db # Importa a classe Password e o banco de dados do arquivo database.py

class PasswordRepository:
    def __init__(self):
        db.connect() # Conecta ao banco de dados
        db.create_tables([Password, Authentication]) # Cria as tabelas no banco de dados, caso ela ainda não exista

    # CRUD(Create, Read, Update, Delete) para manipular os dados do banco de dados utilizando a classe Password

    # Create
    def add(self, title, password):
        # Cria um novo registro de senha no banco de dados utilizando a classe Password
        Password.create(title=title, password=password) 

    # Read
    def list(self):
        # Retorna todas as senhas armazenadas no banco de dados
        return Password.select()
    
    # Update
    def update(self, id, new_password):
        senha = Password.get(Password.id == id)
        senha.password = new_password
        senha.save()

    # Delete
    def delete(self, id):
        senha = Password.get(Password.id == id)
        senha.delete_instance()

    # Deleta completamente todos os dados da tabela para criar uma nova de acordo com o cadastro
    def new_register(self):
        Password.delete().execute()

    # Deleta completamente a autenticação e o salt para criar uma nova de acordo com o cadastro
    def new_auth(self):
        Authentication.delete().execute()

    # Adiciona o salt e o token de segurança para entrar na conta
    def add_auth(self, salt, safe_token):
        Authentication.create(salt=salt, auth=safe_token)
