from conexao import *
from read import *
from create import *
from editar import editar
from deletar import deletar

def menu():
    conexao = conecta()
    while True:
        print('-' * 30)
        print("Sistema Cyntax".center(30))
        print('-' * 30)
        print("O que Deseja Fazer?")
        print("[1] Listar Alunos\n[2] Adicionar Novo Alunos\n" \
        "[3] Editar Aluno\n[4] Deletar Aluno\n[5] Sair")

        while True:
            resp = input(' ')
            if resp.isnumeric():
                resp = int(resp)
                break
            print('Opção inválida! Digite um número existente no menu.')

        match resp:
            case 1:
                read(conexao)
            case 2:
                create(conexao)
            case 3:
                editar(conexao)
            case 4:
                deletar(conexao)
            case 5:
                conexao.close()
                print('Encerrando o sistema. . .')
                break