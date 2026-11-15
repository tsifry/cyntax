# O editar problemas acontece usando chaves compostas, incrementando tentativas e tempo gasto.
import hashlib

def editar(conexao, tabela):
    cursor = conexao.cursor()
    try:
        if tabela == 'Usuarios':
            id_usuario = int(input('Digite o ID do usuário que deseja editar: '))
            nome = input('Novo NOME: ')
            email = input('Novo EMAIL: ')
            foto = input('Nova FOTO_PERFIL: ')
            assinante = True if input('Assinante? [S/N]: ').upper() == 'S' else False

            sql = "UPDATE Usuarios SET NOME=%s, EMAIL=%s, FOTO_PERFIL=%s, ASSINANTE=%s WHERE ID=%s"
            cursor.execute(sql, (nome, email, foto if foto else None, assinante, id_usuario))

        elif tabela == 'Autenticacao':
            id_usuario = int(input('Digite o ID: '))
            senha = input('Digite a nova SENHA: ')
            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            sql = "UPDATE Autenticacao SET SENHA=%s WHERE ID_USUARIO=%s"
            cursor.execute(sql, (senha_hash, id_usuario))

        elif tabela == 'Modulos':
            id_modulo = int(input('Digite o ID do Módulo: '))
            nome = input('Novo NOME: ')
            dificuldade = input("Nova DIFICULDADE: ")
            assinante = True if input("Exclusivo para assinantes? (S/N): ").upper() == 'S' else False

            sql = "UPDATE Modulos SET NOME=%s, DIFICULDADE=%s, ASSINANTE=%s WHERE ID=%s"
            cursor.execute(sql, (nome, dificuldade, assinante, id_modulo))

        elif tabela == 'Problemas':
            id_problema = int(input('Digite o ID do problema: '))
            descricao = input('Nova DESCRIÇÃO: ')

            sql = "UPDATE Problemas SET DESCRICAO=%s WHERE ID=%s"
            cursor.execute(sql, (descricao, id_problema))

        elif tabela == 'Jogos':
            id_jogo = int(input('Digite o ID do Jogo: '))
            descricao = input('Nova DESCRICAO: ')
            sandbox = True if input('É SandBox? [S/N]: ').upper() == 'S' else False

            sql = "UPDATE Jogos SET DESCRICAO=%s, SANDBOX=%s WHERE ID=%s"
            cursor.execute(sql, (descricao, sandbox, id_jogo))

        elif tabela == 'ProgressoProblemas':
            id_usuario = int(input('Digite o ID do usuario: '))
            id_problema = int(input('Digite o ID do problema: '))
            tempo_gasto = int(input("Tempo gasto adicional (segundos):" ))
            finalizado = True if input('O problema foi finalizado agora? [S/N]: ').upper() == 'S' else False

            sql = """UPDATE ProgressoProblemas 
                     SET TENT_TOTAIS = TENT_TOTAIS + 1, 
                         TEMPO_GASTO = TEMPO_GASTO + %s, 
                         FINALIZADO = %s 
                     WHERE ID_USUARIO=%s AND ID_PROBLEMA=%s"""
            cursor.execute(sql, (tempo_gasto, finalizado, id_usuario, id_problema))

        elif tabela == 'ProgressoJogos':
            id_usuario = int(input("Digite o ID_USUARIO: "))
            id_jogo = int(input("Digite o ID_JOGO: "))
            highscore = int(input('Pontuação do Highscore: '))
            tempo_jogado = int(input('Tempo jogado adicional (segundos): '))
            
            sql = """UPDATE ProgressoJogos 
                     SET JOGADOS = JOGADOS + 1, 
                         HIGHSCORE = HIGHSCORE + %s, 
                         TEMPO_JOGADO = TEMPO_JOGADO + %s 
                     WHERE ID_USUARIO=%s AND ID_JOGO=%s"""
            cursor.execute(sql, (highscore, tempo_jogado, id_usuario, id_jogo))

        elif tabela == 'Ranking':
            id_usuario = int(input('Digite o ID do Usuário: '))
            temporada = int(input('Temporada: '))
            pontos = int(input('Pontos a somar na pontuação: '))

            sql = "UPDATE Ranking SET PONTUACAO = PONTUACAO + %s WHERE ID_USUARIO=%s AND TEMPORADA=%s"
            cursor.execute(sql, (pontos, id_usuario, temporada))

        else:
            print(f'Não há operação de edição configurada para a tabela {tabela}')
            return

        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Registro em {tabela} atualizado com sucesso!')
        else:
            print("Nenhum registro encontrado...")

    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar atualizar a tabela {tabela}: {e}')
    finally:
        cursor.close()