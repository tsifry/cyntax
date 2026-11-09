def editar(conexao):
    cursor = conexao.cursor()

    id_aluno = int(input('Digite o ID do aluno que deseja editar: '))
    novo_nome = input('Digite o novo nome do aluno: ')
    nova_idade = int(input('Digite a nova idade do aluno: '))

    sql = """
    UPDATE alunosPI
    SET nome = %s, idade = %s
    WHERE id = %s
    """

    cursor.execute(sql, (novo_nome, nova_idade, id_aluno))
    conexao.commit()

    if cursor.rowcount > 0:
        print(f'Aluno com ID {id_aluno} atualizado com sucesso!')
    else:
        print(f'Aluno com ID {id_aluno} não encontrado!')

    cursor.close()