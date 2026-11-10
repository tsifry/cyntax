# O editar problemas acontece usando chaves compostas, incrementando tentativas e tempo gasto.
def editarProblema(conexao, id_usuario, id_problema, tempo_gasto_adicional, finalizou):
    cursor = conexao.cursor()

    # Utilizado para conversão do booleando para 1 ou 0 no banco de dados
    statusFinalzado = 1 if finalizou else 0

    sql = """
    UPDATE Progresso_Problemas 
    SET TENT_TOTAIS = TENT_TOTAIS + 1, 
        TEMPO_GASTO = TEMPO_GASTO + %s,
        FINALIZADO = %s
    WHERE ID_USUARIO = %s AND ID_PROBLEMA = %s
    """
    valores = (tempo_gasto_adicional, statusFinalzado, id_usuario, id_problema)

    try:
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Progresso do problema {id_problema} atualizado com sucesso para o usuário {id_usuario}.')
        else:
            print(f'Nenhum registro encontrado!')
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar atualizar o progresso do problema: {e}')
    finally:
        cursor.close()

# Atuliza a pontuação do usuário no raking daquela temporada
def atualizarPontuacao(conexao, id_usuario, temporada, pontosConquistados):
    cursor = conexao.cursor()
    sql = """
    UPDATE Ranking 
    SET PONTUACAO = PONTUACAO + %s
    WHERE ID_USUARIO = %s AND TEMPORADA = %s
    """
    try:
        cursor.execute(sql, (pontosConquistados, id_usuario, temporada))
        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Foram adicionados {pontosConquistados} pontos ao usuário {id_usuario}.')
        else:
            print(f'Nenhum registro encontrado para o usuário {id_usuario} na temporada {temporada}.')
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar atualizar a pontuação do usuário: {e}')
    finally:
        cursor.close()

# Atualiza os dados de um perfil de usuário, como nome, email, foto e status de assinatura.
def editarUsuario(conexao, id_usuario, novo_nome, novo_email, nova_foto, status_assinante):
    cursor = conexao.cursor()

    # status_assinante sempre será um booleano, então convertemos para 1 ou 0 para o banco de dados
    # status_assinante deve ser um booleano (True/False) ou 1/0
    sql = """
    UPDATE Usuarios 
    SET NOME = %s, 
        EMAIL = %s, 
        FOTO_PERFIL = %s, 
        ASSINANTE = %s
    WHERE ID = %s
    """

    valores = (novo_nome, novo_email, nova_foto, 1 if status_assinante else 0, id_usuario)

    try:
        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            print(f'Perfil do usuário {id_usuario} atualizado com sucesso.')
        else:
            print(f'Nenhum usuário encontrado com ID: {id_usuario}')
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar atualizar o perfil do usuário: {e}')
    finally:
        cursor.close()

# Atualiza a senha de um usuário no banco de dados.
def editarSenha(conexao, id_usuario, nova_senha):
    cursor = conexao.cursor()
    
    sql = """
    UPDATE Autenticacao 
    SET SENHA = %s 
    WHERE ID_USUARIO = %s
    """

    try:
        cursor.execute(sql, (nova_senha, id_usuario))
        conexao.commit()
        if cursor.rowcount > 0:
            print(f'Senha do usuário {id_usuario} atualizada com sucesso.')
        else:
            print(f'Nenhum usuário encontrado com ID: {id_usuario}')
    except Exception as e:
        conexao.rollback()
        print(f'Erro ao tentar atualizar a senha do usuário: {e}')
    finally:
        cursor.close()