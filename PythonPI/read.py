def read(conexao):
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * from alunosPI")

    itens = cursor.fetchall()

    for item in itens:
        #maneira de printar bonitinho a tabela.
        #talvez fazendo do jeito do lucio.
        pass

    cursor.close()