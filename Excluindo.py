def Dell():
    import sqlite3

    conn = sqlite3.connect("BancoLocal.db")
    cursor = conn.cursor()

    id_delete = input("entre com o id para deletar: ")
        
    cursor.execute("""DELETE FROM login WHERE id = ?""",(id_delete,))
    cursor.execute("""DELETE FROM bloco WHERE id = ?""",(id_delete,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Usuário deletado com sucesso")
    else:
        print(f"Usuário de id {id_delete} não encontrado")