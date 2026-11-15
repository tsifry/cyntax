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
    print("Digite o campo: ")
    match tabela:
        case "Usuarios":
            print("[1] ID\n[2] EMAIL")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"EMAIL": input("Digite o EMAIL: ")}
            
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)

        case "Autenticacao":#na teoria eh isso. tem que ver se o return vai dar de fato 1 numero
            email = input('Digite o email para consulta: ')
            idUsuario = consulta(conexao, "Usuarios", filtro={"EMAIL": email})

            resultado = consulta(conexao, tabela, filtro={"ID_USUARIO": idUsuario[0]['ID']})
            exibe(resultado)
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
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "Problemas":#AQUI TERIA O RESPOSTA TAMBEM
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "Jogos":
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "ProgressoProblemas":
            print("[1] ID_USUARIO\n[2] ID_USUARIO + ID_PROBLEMA")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                           "ID_PROBLEMA": int(input("Digite o ID_PROBLEMA: "))}
                
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "ProgressoJogos":
            print("[1] ID_USUARIO\n[2] ID_USUARIO + ID_JOGO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                           "ID_JOGO": int(input("Digite o ID_JOGO: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "PontuacaoHistorico":
            filtro = {"ID_USUARIO": int(input("Digite o ID do usuario: "))}
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)
        case "Ranking":
            print("[1] TEMPORADA\n[2] ID_USUARIO + TEMPORADA")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"TEMPORADA": int(input("Digite a TEMPORADA: "))}
            else:
                filtro = {"ID_USUARIO": int(input("Digite o ID_USUARIO: ")),
                          "TEMPORADA": int(input("Digite a TEMPORADA: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)
            exibe(resultado)

#monta o comando select
def consulta(conexao, tabela, colunas = None, filtro=None):
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
        sql += f" ORDER BY `TEMPORADA` DESC"

        sql += " LIMIT %s"
        while True:
            limit = int(input('LIMIT: '))
            if isinstance(limit, int):
                break
        valores.append(limit)

    try:
        cursor = conexao.cursor(dictionary = True)
        cursor.execute(sql, tuple(valores))

        resultados = cursor.fetchall()

        return resultados
    except Exception as erro:
        print(f"Ocorreu o erro: {erro}")
        input()
        return []

    finally:
        cursor.close()
        conexao.close() 

def exibe(resultado):
    print('-' * 120)
    tamanho = calctamanho(resultado)
    for indice, chave in enumerate(resultado[0].keys()):
        print(f"{chave:^{tamanho[indice]}}|", end='')
    print()

    print('-' * 120)
    for i in range(len(resultado)):
        for indice, valor in enumerate(resultado[i].values()):
            print(f"{str(valor):^{tamanho[indice]}}|", end='')
        print()
    print('-' * 120)

    input()

def calctamanho(resultado):
    tamanho = []
    chaves = []
    valores = []
    #pega o tamanho de todas as chaves
    for chave in resultado[0].keys():
        chaves.append(len(chave) + 2)

    #pega o tamanho de todos os valores
    for i in range(len(resultado)):
        valor = []
        for value in resultado[i].values():
            valor.append(len(str(value)))

        valores.append(valor)

    valoresfinais = []

    #pega o maior dos tamanhos dos valores de cada coluna da tabela
    for v in range(len(valores) - 1):
        for c in range(len(chaves)):
            maior = max(valores[v][c], valores[v+1][c])
            valoresfinais.append(maior + 2)

    #caso só tenha um registro na tabela
    if len(valoresfinais) == 0:
        valoresfinais = valores[0][:]

    #monta os tamanho finais que serão usados em cada coluna
    for i in range(len(chaves)):
        tamanho.append(max(chaves[i], valoresfinais[i]))

    return tamanho