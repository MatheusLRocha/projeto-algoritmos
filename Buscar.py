import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()

id_busca = input("coloque algum id: ")

cursor.execute("""SELECT nome, email, senha_login FROM login WHERE id = ?""",(id_busca,))

login = cursor.fetchone()

if login:
    print(f"Usuário encontrado: {login[0]} ({login[1]})")
else:
    print(f"Usuário não encontrado")

