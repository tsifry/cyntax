def deletar(conexao):
    cursor = conexao.cursor()

    id_aluno = int(input('Digite o ID do aluno que deseja deletar: '))
    sql = "DELETE FROM alunosPI WHERE id = %s"

    cursor.execute(sql, (id_aluno,))
    conexao.commit()

    if cursor.rowcount > 0:
        print(f'Aluno com ID {id_aluno} deletado com sucesso!')
    else:
        print(f'Aluno com ID {id_aluno} não encontrado!')

    cursor.close()