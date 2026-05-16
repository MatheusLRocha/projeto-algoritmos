import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()

nome = input("Digite o nome de usuário: ")
email = input("Digite o seu email: ")
senha_login = input("Digite uma Senha: ")
titulo = input("Digite um titulo para o bloco: ")
senha_bloco = input("Digite uma Senha para o bloco: ")
anotacoes = input("Escreva uma anotação para o bloco: ")

#AS SENHAS ESTÂO SEM NOT NULL POR QUE TEM QUE APRENDER A MEXer NO BYcrypt

cursor.execute("""CREATE TABLE IF NOT EXISTS login (
               id iNTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome VARCHAR(100) NOT NULL,
               email VARCHAR(100) NOT NULL UNIQUE,
               senha_login BLOB 
               );""")
cursor.execute("""  CREATE TABLE IF NOT EXISTS bloco_senha (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               titulo VARCHAR(100),
               senha_bloco BLOB,
               anotacoes TEXT,
               FOREIGN KEY (id_usuario) REFERENCES login(id)
               );""")

cursor.execute("""INSERT INTO login (nome, email, senha_login) values (?,?,?)""",(nome, email, senha_login))
cursor.execute("""INSERT INTO bloco_senha (titulo, senha_bloco, anotacoes) values (?,?,?)""",(titulo, senha_bloco, anotacoes))

conn.commit()

print(f"Usuário {nome} cadastrado com sucesso")

conn.close()
#OBS: exemplo de como responder a erros sem fechar o programa
# try:
#     cursor.execute("""INSERT INTO login (nome,email) values (?,?)""",(nome, email))
#     conn.commit()
    
#     print(f"")

# except sqlite3.IntegrityError: 
#     print("Erro: Este Email já está cadastrado")
# except Exception as e:
#     print(f"Ocorreu um erro: {e}")
