from tabelas import TABELAS
import hashlib
from geracsv import geraCsv
from consultacsv import consultaCsv
from mysql.connector import Error

#cria novo registro na tabela.
def inserir(conexao, tabela):
    if tabela not in TABELAS:
        print('Tabela não cadastrada.')
        input('[ENTER] para continuar')
        return

    dados = {}

    for campo, tipo, regra in TABELAS[tabela]:
        if regra == "AUTO":
            continue

        if regra == "NOT_NULL":
            valor = input(f'informe {campo}: ')

            while valor == "":
                print('Este campo é obrigatório!')
                valor = input(f'informe {campo}: ')

            if campo == "SENHA":
                valor = hashlib.sha256(valor.encode('utf-8')).hexdigest()

            dados[campo] = valor

        elif regra == "NULL":
            valor = input(f"informe {campo} (opcional [ENTER]): ")

            if valor == "":
                valor = None

            dados[campo] = valor

        elif regra == "DEFAULT":
            valor = input(f"informe {campo} ([ENTER] para usar o valor padrão): ").strip()

            #if valor verifica se a variavel está vazia
            if valor:
                dados[campo] = valor

        try:
            if valor:
                dados[campo] = tipo(valor)

        except:
            print(f"Valor inválido para {campo}: {valor}")
            input('[ENTER] para continuar')
            return

    campos = list(dados.keys())

    colunas = ", ".join(f"{campo}" for campo in campos)
    recebevalores = ", ".join(["%s"] * len(campos))

    sql = f"""
        INSERT INTO `{tabela}` ({colunas})
        VALUES({recebevalores})
        """

    geraCsv(tabela, dados)

    valores = consultaCsv(tabela)

    try:
        cursor = conexao.cursor()
    
        cursor.execute(sql, tuple(valores))
        conexao.commit()
        print('produto cadastrado com sucesso!')
        input()
    except Error as erro:
        print(f'Ocorreu o erro: {erro}')
        input()
        return None

    cursor.close()