from tabelas import TABELAS
import hashlib
from mysql.connector import Error
import csv
from read import escolha
import os

def create(conexao, tabela: str) -> None:
    while True:
        print("Escolha uma das opções:")
        print("[1] Coletar os dados para criar o CSV.\n" \
        "[2] Carregar os dados do CSV no MySQL.\n" \
        "[3] Sair\n")

        escolhida = escolha(3)#validar entrada do usuario.

        match escolhida:
            case 1: escrever_csv(tabela)
            case 2: carregar_csv_no_mysql(conexao, tabela)
            case 3: break

#escreve novas linhas no arquivo csv.
def escrever_csv(tabela: str) -> None:
    arquivo = tabela + '.csv'
    dados = {}
    while True:
        dados.clear()
        print('escreva sair para encerrar.')
#tirar o tipo se der certo
        for campo, regra in TABELAS[tabela]:
            if regra == "AUTO":#caso o campo seja auto_increment ele para e vai pro próximo campo.
                continue

            if regra == "NOT_NULL":#não deixa o usuario continuar sem fornecer o dado pedido.
                valor = input(f'informe {campo}: ')

                while valor == "":
                    print('Este campo é obrigatório!')
                    valor = input(f'informe {campo}: ')

                if campo == "SENHA":#em caso de ser senha, armaneza o hash dela e não ela de fato.
                    valor = hashlib.sha256(valor.encode('utf-8')).hexdigest()

                dados[campo] = valor

            elif regra == "NULL":#campo pode ficar em branco.
                valor = input(f"informe {campo} (opcional [ENTER]): ")

                if valor == "":
                    valor = "None"

                dados[campo] = valor

            elif regra == "DEFAULT":#opção de escolher o valor padrão
                valor = input(f"informe {campo} ([ENTER] para usar o valor padrão): ").strip()

                #if valor verifica se a variavel está vazia
                if valor:
                    dados[campo] = valor

            if str(valor).lower() == 'sair':#caso o usuario digite sair sai do laço for de novos registros.
                break


        if str(valor).lower() == 'sair':#e sai do while true principal.
            break

        #escreve de fato no arquivo csv.
        with open(arquivo, mode='a', newline='', encoding='utf-8') as arq:
                escritor = csv.writer(arq)

                escritor.writerow(dados.keys())#escreve as colunas que foram usadas.
                escritor.writerow(dados.values())#escreve os valores das colunas.
                print("Salvo no CSV!\n")


def carregar_csv_no_mysql(conexao, tabela: str, ) -> None:
    arquivo = tabela + '.csv'
    tabelafinal = 'g07_' + tabela#coloquei assim para manter a estrutura usando o tabela, mas fazer
#                                 o commit na tabela com esse nome como o banin pediu.

    if not os.path.exists(arquivo):
        print(f'arquivo {arquivo} não encontrado.')
        return
    
    valoresfinais = []#lista de valores que serão usados no cursor.execute

    try:
        cursor = None
#aqui a logica usada foi linhas impares guardarem os nomes das colunas que serão usadas e as pares os valores.
        with open(arquivo, mode='r', newline='', encoding='utf-8') as arq:
            linhas = list(csv.reader(arq))
            
            if len(linhas) % 2 != 0:
                print("Algum registro não informou suas colunas ou seus valores. Corrija para retornar.")
                return

            for i in range(0, len(linhas), 2):
                valoresfinais.clear()

                colunas = linhas[i]
                colunaslimpa = ", ".join(colunas)#nomes das colunas sem aspas simples.
                valores = linhas[i+1] 

                recebevalores = ", ".join(["%s"] * len(colunas))#monta quantos $s aparecerão no comando sql
                
                sql = f'''INSERT IGNORE INTO `{tabelafinal}`
                    ({colunaslimpa})
                    VALUES ({recebevalores})
                '''

                for item in valores:#validações de tipos
                    if item == 'True':
                        valoresfinais.append(True)
                    elif item == 'False':
                        valoresfinais.append(False)
                    elif item == 'None':
                        valoresfinais.append(None)
                    elif item.isnumeric():
                        valoresfinais.append(int(item))
                    else:
                        valoresfinais.append(item)

                cursor = conexao.cursor()
                cursor.execute(sql, valoresfinais)

    except Exception as e:
        print('[Exceção ao carregar CSV no MySQL]')
        print(f'Descrição: {e}')
    else:
        conexao.commit()
        print('Dados carregados no MySQL!')
    finally:
        if cursor is not None:
            cursor.close()