from tabelas import TABELAS

#valida entradas do usuário
def escolha(qtdOpcoes):
    while True:
        while True:
            escolhida = input(' ')
            if escolhida.isnumeric():
                escolhida = int(escolhida)
                break
            else:
                print("A entrada deve ser do tipo inteiro.")
                input('[ENTER] para digitar novamente')

        if escolhida > 0 and escolhida <= qtdOpcoes:
            break
        else:
            print('A entrada deve ser um número inteiro que corresponda a uma das tabelas.')
            input('[ENTER] para digitar novamente')
            continue

    return escolhida

#organiza e direciona para a criação do comando select
def read(conexao, tabela):
    colunas = None
    filtro = None
    print("Por qual campo deseja realizar a consulta?")
    match tabela:
        case "Usuarios":
            print("[1] ID\n[2] EMAIL")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"EMAIL": input("Digite o EMAIL: ")}
            
            resultados = select(conexao, tabela, colunas, filtro)
            print(resultados)

        case "Autenticacao":#na teoria eh isso. tem que ver se o return vai dar de fato 1 numero
            email = input('Digite o email para consulta: ')
            idUsuario = select(conexao, "Usuarios", ["ID"], {"EMAIL": {email}})
            sql = f"SELECT hash from `Autenticacao WHERE ID_USUARIO = {idUsuario}"
            executa(conexao, sql, [idUsuario])
        case "Modulos":
            print("[1] DIFICULDADE\n[2] NOME\n[3] ASSINANTE")
            escolhida = escolha(3)
            if escolhida == 1:
                filtro = {"DIFICULDADE": input("Digite a DIFICULDADE: ")}
            elif escolhida == 2:
                filtro = {"NOME": input("Digite o NOME: ")}
            else:
                print("Módulo exclusivo para assinantes?\n[1] Sim\n[2] Não\n")
                escolhida = escolha(2)
                if escolhida == 1:
                    filtro = {"ASSINANTE": True}
                else:
                    filtro = {"ASSINANTE": False}
            select(conexao, tabela, colunas, filtro)
        case "Problemas":#AQUI TERIA O RESPOSTA TAMBEM
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            select(conexao, tabela, colunas, filtro)
        case "Jogos":
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            select(conexao, tabela, colunas, filtro)
        case "ProgressoProblemas":
            print("[1] ID_USUARIO\n[2] ID_USUARIO + ID_PROBLEMA")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                           "ID_PROBLEMA": int(input("Digite o ID_PROBLEMA: "))}
                
            select(conexao, tabela, colunas, filtro)
        case "ProgressoJogos":
            print("[1] ID_USUARIO\n[2] ID_USUARIO + ID_JOGO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                           "ID_JOGO": int(input("Digite o ID_JOGO: "))}
            
            select(conexao, tabela, colunas, filtro)
        case "PontuacaoHistorico":
            filtro = {"ID_USUARIO": int(input("Digite o ID do usuario para a busca"))}
            select(conexao, tabela, colunas, filtro)
        case "Ranking":
            print("[1] TEMPORADA\n[2] ID_USUARIO + TEMPORADA")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"TEMPORADA": int(input("Digite a TEMPORADA: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                          "TEMPORADA": int(input("Digite a TEMPORADA: "))}
            
            select(conexao, tabela, colunas, filtro)

#monta o comando select
def select(conexao, tabela, colunas = None, filtro=None):
    if tabela not in TABELAS:
        print('tabela não encontrada!')
        return

    camposValidos = {campo for campo, tipo, regra in TABELAS[tabela]}

    if colunas is not None:

        if not isinstance(colunas, list):
            print("colunas deve ser uma lista!")
            return
        
        colunasInvalidas = [campo for campo in colunas if campo not in camposValidos]

        if colunasInvalidas:
            print(f"colunas inválidas: {colunasInvalidas}")
            return

    if colunas is None:
        selecionados = "*"
    else:
        selecionados = ", ".join(f"`{campo}`" for campo in colunas)

    sql = f"SELECT {selecionados} FROM `{tabela}`"

    if filtro is not None:
        if not isinstance(filtro, dict):
            print("filtro precisa ser um dicionario!")
            return

        filtrosInvalidos = [
            campo for campo in filtro if campo not in camposValidos
        ]

        if filtrosInvalidos:
            print(f"Filtros Inválidos: {filtrosInvalidos}")
            input()
            return

        condicoes = []
        valores = []

    if filtro:
        for campo, valor in filtro.items():
            if valor is None:
                condicoes.append(f"`{campo}` IS NULL")
            else:
                condicoes.append(f"`{campo}` = %s")
                valores.append(valor)

    if condicoes:
        sql += " WHERE " + " AND ".join(condicoes)

    if tabela == "Ranking":
        sql += f" ORDER BY `TEMPORADA` `DESC`"

        sql += " LIMIT %s"
        while True:
            limit = int(input())
            if isinstance(limit, int):
                break
        valores.append(limit)

    resultados = executa(conexao, sql, valores)

    return resultados

#executa o comando select
def executa(conexao, sql, valores):
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(sql, tuple(valores))

        resultados = cursor.fetchall()

        return resultados
    except Exception as erro:
        print(f"Ocorreu o erro: {erro}")
        input()

    finally:
        cursor.close()