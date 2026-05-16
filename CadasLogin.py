import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()

nome = input("Digite o nome de usuário: ")
email = input("Digite o seu email: ")
senha_login = input("Digite uma Senha: ")
titulo = input("Digite um titulo para o bloco: ")
senha_bloco = input("Digite uma Senha para o bloco: ")
anotacoes = input("Escreva uma anotação para o bloco: ")
try:
    cursor.execute("""INSERT INTO login (nome, email, senha_login) values (?,?,?)""",(nome, email, senha_login))

    id_usuario = cursor.lastrowid

    cursor.execute("""INSERT INTO bloco (titulo, senha_bloco, anotacoes, id_usuario) values (?,?,?,?)""",(titulo, senha_bloco, anotacoes, id_usuario))

    conn.commit()

    print(f"Usuário {nome} cadastrado com sucesso")

    conn.close()
except sqlite3.IntegrityError:
    print("Erro: Este Email já está cadastrado")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

