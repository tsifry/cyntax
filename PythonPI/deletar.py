# Deleta o usuário e todos os registros relacionados em cascata
def deletarUsuario(conexao, id_aluno):
    cursor = conexao.cursor()
    try:
        # Primeiro deleta os "filhos" relacionados ao usuário
        queriesFilhas = [
            "DELETE FROM Ranking WHERE ID_USUARIO = %s",
            "DELETE FROM PontuacaoHistorico WHERE ID_USUARIO = %s",
            "DELETE FROM ProgressoJogos WHERE ID_USUARIO = %s",
            "DELETE FROM Progresso_Problemas WHERE ID_USUARIO = %s",
            "DELETE FROM Autenticacao WHERE ID_USUARIO = %s"
        ]

        for query in queriesFilhas:
            cursor.execute(query, (id_aluno,))
        # Deleta o usuário em seguida
        cursor.execute("DELETE FROM Usuarios WHERE ID = %s", (id_aluno,))

        # Envia as alterações para o banco de dados
        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Usuário com ID {id_aluno} e todos os registros relacionados foram deletados com sucesso.')
        else:
            print(f'Nenhum usuário encontrado com ID: {id_aluno}')

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar deletar o usuário {id_aluno}: {e}')
    finally:
        cursor.close()

# Tenta deletar o probema se não houver progresso de aluno vinculado a ele
def deletarProblema(conexao, id_problema):
    cursor = conexao.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM Progresso_Problemas WHERE ID_PROBLEMA = %s', (id_problema,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            print('Impossível deletar o problema, existem alunos com progresso vinculado!')
            return

        cursor.execute('DELETE FROM Problemas WHERE ID = %s', (id_problema,))
        conexao.commit()
        print(f'Problema {id_problema} deletado com sucesso!')

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar deletar o problema {id_problema}: {e}')
    finally:
        cursor.close()