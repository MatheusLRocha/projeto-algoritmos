from database import Password, db # Importa a classe Password e o banco de dados do arquivo database.py

class ConexaoBancoDeDados:
    def __init__(self):
        db.connect() # Conecta ao banco de dados
        db.create_tables([Password]) # Cria a tabela de senhas no banco de dados, caso ela ainda não exista

    # CRUD(Create, Read, Update, Delete) para manipular os dados do banco de dados utilizando a classe Password

    def adicionar_senha(self, title, password):
        # Cria um novo registro de senha no banco de dados utilizando a classe Password
        Password.create(title=title, password=password) 

    def listar_senhas(self):
        # Retorna todas as senhas armazenadas no banco de dados
        return Password.select()
    
    def buscar_senha(self, title):
        return Password.get_or_none(Password.title == title)
    
    def atualizar_senha(self, title, new_password):
        ...

    def deletar_senha(self, title):
        ...

        


        
        



