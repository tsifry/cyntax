from tabelas import TABELAS

#valida escolha do usuário.
def escolha(qtdOpcoes: int) -> int:
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

#organiza as consultas de acordo com o que cada tabela permite.
def read(conexao, tabela: str) -> None:
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

            if resultado != None:
                exibe(resultado)

        case "Autenticacao":
            email = input('Digite o email para consulta: ')
            idUsuario = consulta(conexao, "Usuarios", filtro={"EMAIL": email})

            if len(idUsuario) == 0:
                print("Erro! A lista que recebeu os resultados da busca está vazia.")
                input()
                return

            resultado = consulta(conexao, tabela, filtro={"ID_USUARIO": idUsuario[0]['ID']})
            
            if resultado != None:
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

            if resultado != None:
                exibe(resultado)

        case "Problemas":#AQUI TERIA O RESPOSTA TAMBEM
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)

            if resultado != None:
                exibe(resultado)

        case "Jogos":
            print("[1] ID\n[2] ID_MODULO")
            escolhida = escolha(2)
            if escolhida == 1:
                filtro = {"ID": int(input("Digite o ID: "))}
            else:
                filtro = {"ID_MODULO": int(input("Digite o ID_MODULO: "))}
            
            resultado = consulta(conexao, tabela, colunas, filtro)

            if resultado != None:
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

            if resultado != None:
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

            if resultado != None:
                exibe(resultado)

        case "PontuacaoHistorico":
            filtro = {"ID_USUARIO": int(input("Digite o ID do usuario: "))}
            resultado = consulta(conexao, tabela, colunas, filtro)

            if resultado != None:
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

            if resultado != None:
                exibe(resultado)

#monta e tenta executar o comando sql.
def consulta(conexao, tabela: str, colunas: list = None, filtro: dict =None) -> list | None:
    #verifica se a consulta deve ser feita através de colunas especificas ou se deve pegar todos os campos (*).
    if colunas is None:
        selecionados = "*"
    else:
        selecionados = ", ".join(f"`{campo}`" for campo in colunas)

    sql = f"SELECT {selecionados} FROM `{tabela}`"#monta primeira parte do comando sql de consulta.

    if filtro is not None:#filtro serve para buscar registros na tabela por algum valor em específico.
        if not isinstance(filtro, dict):
            print("filtro precisa ser um dicionario!")
            return

        condicoes = []#lista que irá armazenar as condições que serão colocadas no comando WHERE.
        valores = []#valores das condições.

    #monta as strings que serão usadas no comando WHERE de fato.
        for campo, valor in filtro.items():
            if valor is None:
                condicoes.append(f"{campo} IS NULL")
            else:
                condicoes.append(f"{campo} = %s")
                valores.append(valor)

    if condicoes:#verifica se condições não está vazia e adiciona no comando sql a parte das condições.
        sql += " WHERE " + " AND ".join(condicoes)

    if tabela == "Ranking":#se for a tabela ranking os valores devem ser mostrados do maior para o menor.
        sql += f" ORDER BY `TEMPORADA` DESC"

        sql += " LIMIT %s"#adiciona a parte do limit no comando sql.
        while True:
            limit = int(input('LIMIT: '))
            if isinstance(limit, int):
                break
        valores.append(limit)

    try:
        cursor = conexao.cursor(dictionary = True)
        cursor.execute(sql, tuple(valores))

        resultados = cursor.fetchall()#coloca os resultados da consulta na variavél.

        return resultados
    except Exception as erro:
        print(f"Ocorreu o erro: {erro}")
        input()
        return None

    finally:
        cursor.close()

#função responsável por exibir os resultados como uma tabela no terminal.
def exibe(resultado: list) -> None:
    if len(resultado) == 0:
        print("Erro! A lista que recebeu os resultados da busca está vazia.")
        input()
        return
    
    print('-' * 120)
    tamanho = calctamanho(resultado)#calcula em qual valor deve centralizar cada campo e valor.
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

#calcula em qual valor deve centralizar cada campo e valor.
def calctamanho(resultado: list) -> list:
    tamanho = []#lista que guardará os valores finais que cada campo deve ser centralizado.
    chaves = []#guardará os valores do tamanho dos nomes das chaves para ser usados nos calculos.
    valores = []#guardará os valores de cada registro da tabela.

    #pega o tamanho de todas as chaves
    for chave in resultado[0].keys():
        chaves.append(len(chave) + 2)

    #pega o tamanho de todos os valores
    for i in range(len(resultado)):
        valor = []
        for value in resultado[i].values():
            valor.append(len(str(value)))

        valores.append(valor)

    valoresfinais = []#guardará os finais tamanhos dos maiores valores de cada coluna.

    #pega o maior dos tamanhos dos valores de cada coluna da tabela.
    for v in range(len(valores) - 1):
        for c in range(len(chaves)):
            maior = max(valores[v][c], valores[v+1][c])
            valoresfinais.append(maior + 2)

    #caso só tenha um registro na tabela usa ele para comparação final.
    if len(valoresfinais) == 0:
        valoresfinais = valores[0][:]

    #pega o maior tamanho entre chaves e valores.
    for i in range(len(chaves)):
        tamanho.append(max(chaves[i], valoresfinais[i]))

    return tamanho#retorna a lista contendo os tamanhos que cada coluna deve ter no print da consulta.