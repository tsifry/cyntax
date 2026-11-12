from conexao import conecta
from criatabelas import criatabelas
from tabelas import TABELAS
from read import read
from create import create
#from editar import editar
#from deletar import deletar

def menu():
    conexao = conecta()
    criatabelas(conexao)
    while True:
        print('-' * 30)
        print("Sistema Cyntax".center(30))
        print('-' * 30)
        print("O que Deseja Fazer?")
        print("[1] Listar\n[2] Adicionar\n[3] Editar\n[4] Deletar\n[5] Sair")

        while True:
            resp = input(' ')
            if resp.isnumeric():
                resp = int(resp)
                break
            print('Opção inválida! Digite um número existente no menu.')

        match resp:
            case 1:
                tabela = list(TABELAS.keys())[escolheTabela() - 1]
                read(conexao, tabela)
            case 2:
                tabela = list(TABELAS.keys())[escolheTabela() - 1]
                create(conexao, tabela)
            case 3:
                editar(conexao)
            case 4:
                deletar(conexao)
            case 5:
                conexao.close()
                print('Encerrando o sistema. . .')
                break

def escolheTabela():
    while True:
        print("Qual das tabelas deseja alterar?")
        for i, tabela in enumerate(TABELAS.keys()):
            print(f"[{i+1}] {tabela}")

        while True:
            escolhida = input(' ')
            if escolhida.isnumeric():
                escolhida = int(escolhida)
                break
            else:
                print("A entrada deve ser do tipo inteiro.")
                input('[ENTER] para digitar novamente')

        if escolhida > 0 and escolhida <= len(TABELAS.keys()):
            break
        else:
            print('A entrada deve ser um número inteiro que corresponda a uma das tabelas.')
            input('[ENTER] para digitar novamente')
            continue
        
    return escolhida