from tabelas import TABELAS
import hashlib
from geracsv import geraCsv
from consultacsv import consultaCsv
from mysql.connector import Error

#cria novo registro na tabela.
def inserir(conexao, tabela: str) -> None:
    dados = {}

    for campo, tipo, regra in TABELAS[tabela]:
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
                valor = None

            dados[campo] = valor

        elif regra == "DEFAULT":#opção de escolher o valor padrão
            valor = input(f"informe {campo} ([ENTER] para usar o valor padrão): ").strip()

            #if valor verifica se a variavel está vazia
            if valor:
                dados[campo] = valor

        try:
            if valor:#verifica se a variavel valor não está vazia e atibui o tipo correto a ela.
                dados[campo] = tipo(valor)

        except:
            print(f"Valor inválido para {campo}: {valor}")
            input('[ENTER] para continuar')
            return

    campos = list(dados.keys())#armazena os nomes dos campos.

    colunas = ", ".join(f"{campo}" for campo in campos)#monta o nome das colunas que serão usadas no comando sql.
    recebevalores = ", ".join(["%s"] * len(campos))#monta quantos $s aparecerão no comando sql

    #comando sql pronto para ser combinado com os valores.
    sql = f"""
        INSERT INTO `{tabela}` ({colunas})
        VALUES({recebevalores})
        """

    geraCsv(tabela, dados)#gera o arquivo csv com os dados que o usuario forneceu nos inputs.

    valores = consultaCsv(tabela)#a variavel valores recebe a leitura do arquivo csv.

    try:
        cursor = conexao.cursor()#inicializa cursor.
    
        cursor.execute(sql, tuple(valores))#construção do comando utilizando a string sql e os valores lidos do csv.
        conexao.commit()#executa comando.
        print('produto cadastrado com sucesso!')
        input()
    except Error as erro:
        print(f'Ocorreu o erro: {erro}')#caso ocorra algum erro.
        input()

    cursor.close()#fecha o cursor.