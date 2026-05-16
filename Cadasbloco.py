#Gente nao tenho ideia de como continuar... me ajudem...
#pra deixar claro to tentando fazer os blocos salvos serem puxados pelo id_usuario,
#pra apararecer so pra quem ta logado naquele email os blocos respectivos, mas nao tenho ideia de como proseguir

#os que estao em comentario é oq vai fazer funcionar, to perdido... nem sei se to na ideia certa, ah eu vi uns videos
#pra me ajudar a proseguir, tipo pra saber oq tem que fazer, skskks, sei nada de sqlite

import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()

# nome = input("Digite o nome de usuário: ")
# email = input("Digite o seu email: ")
# senha_login = input("Digite uma Senha: ")
titulo = input("Digite um titulo para o bloco: ")
senha_bloco = input("Digite uma Senha para o bloco: ")
anotacoes = input("Escreva uma anotação para o bloco: ")

# cursor.execute("""INSERT INTO login (nome, email, senha_login) values (?,?,?)""",(nome, email, senha_login))

# id_usuario = cursor.lastrowid


cursor.execute("""INSERT INTO bloco (titulo, senha_bloco, anotacoes, id_usuario) values (?,?,?,?)""",(titulo, senha_bloco, anotacoes, id_usuario))

conn.commit()

print(f"Bloco {titulo} cadastrado com sucesso")

conn.close()



