def deletar(conexao, tabela):
    cursor = conexao.cursor()
    try:
        if tabela == 'Usuarios':
            id_usuario = int(input('Digite o ID do usuário que deseja deletar: '))
            
            # Primeiro deleta os "filhos" relacionados ao usuário
            queriesFilhas = [
                "DELETE FROM Ranking WHERE ID_USUARIO = %s",
                "DELETE FROM PontuacaoHistorico WHERE ID_USUARIO = %s",
                "DELETE FROM ProgressoJogos WHERE ID_USUARIO = %s",
                "DELETE FROM ProgressoProblemas WHERE ID_USUARIO = %s",
                "DELETE FROM Autenticacao WHERE ID_USUARIO = %s"
            ]
            for query in queriesFilhas:
                cursor.execute(query, (id_usuario,))

            # Deleta o usuário em seguida
            cursor.execute("DELETE FROM Usuarios WHERE ID = %s", (id_usuario,))

        elif tabela == 'Problemas':
            id_problema = int(input('Digite o ID do problema: '))

            # Tenta deletar o probema se não houver progresso de aluno vinculado a ele
            cursor.execute('SELECT COUNT(*) FROM ProgressoProblemas WHERE ID_PROBLEMA=%s', (id_problema,))
            if cursor.fetchone()[0] > 0:
                print('Impossível deletar o problema, existem alunos com progresso vinculado!')
                return
            cursor.execute('DELETE FROM Problemas WHERE ID = %s', (id_problema,))

        elif tabela == 'Jogos':
            id_jogo = int(input('Digite o ID do Jogo: '))

            # Tenta deletar se não houver progresso de aluno vinculado a ele
            cursor.execute('SELECT COUNT(*) FROM ProgressoJogos WHERE ID_JOGO = %s', (id_jogo,))
            if cursor.fetchone()[0] > 0:
                print('Impossível deletar o jogo, existem alunos com progresso vinculado!')
                return
            cursor.execute('DELETE FROM Jogos WHERE ID = %s', (id_jogo,))

        elif tabela == 'Modulos':
            id_modulo = int(input('Digite o ID do Módulo: '))
            cursor.execute('DELETE FROM Modulos WHERE ID=%s', (id_modulo,))
        elif tabela in ['ProgressoProblemas', 'ProgressoJogos', 'PontuacaoHistorico', 'Ranking']:
            id_usuario = int(input(f'Digite o ID do Usuário para deletar os registros em {tabela}: '))
            cursor.execute(f"DELETE FROM {tabela} WHERE ID_USUARIO = %s", (id_usuario,))
        else:
            print(f'Não há operação de exclusão configurada para a tabela {tabela}')

        # Envia as alterações para o banco de dados
        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Registro(s) em {tabela} deletado(s) com êxito!')
        else:
            print(f'Nenhum deletado...')

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar deletar dados da tabela {tabela}: {e}')
    finally:
        cursor.close()