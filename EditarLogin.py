import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()


id_busca = input("coloque algum id: ")

novo_nome = input("Atualize o nome de usuário: ")
novo_email = input("Atualize o seu email: ")
nova_senha_login = input("Atualize a senha para login: ")

cursor.execute("""UPDATE login SET email = ?, nome = ?, senha_login = ? WHERE id = ?""",(novo_email, novo_nome, nova_senha_login, id_busca))

conn.commit()

login = cursor.fetchone

conn.close()

if login:
    print(f"Usuário editado com sucesso")
else:
    print(f"Usuário não foi encontrado")