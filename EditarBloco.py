import sqlite3

conn = sqlite3.connect("BancoLocal.db")
cursor = conn.cursor()

id_busca = input("coloque algum id: ")

novo_titulo = input("Atualize o titulo do bloco: ")
nova_senha_bloco = input("Atualize a Senha do bloco: ")
nova_anotacoes = input("Atualize a anotação do bloco: ")

cursor.execute("""UPDATE bloco SET titulo = ?, senha_bloco = ?, anotacoes = ? WHERE id = id = ?""",(novo_titulo, nova_senha_bloco, nova_anotacoes, id_busca))

conn.commit()

bloco = cursor.fetchone

conn.close()

if bloco:
    print(f"Usuário editado com sucesso")
else:
    print(f"Usuário não foi encontrado")

