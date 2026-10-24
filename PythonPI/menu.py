from listar import listar
from adicionar import adicionar
from editar import editar
from deletar import deletar

def menu():
    while True:
        print('-' * 30)
        print("Sistema Cyntax".center(30))
        print('-' * 30)
        print("O que Deseja Fazer?")
        print("[1] Listar Alunos\n[2] Adicionar Novo Alunos\n" \
        "[3] Editar Aluno\n[4] Deletar Aluno\n[5] Sair")

        while True:
            resp = int(input())
            if resp.isnumeric():
                break

        match resp:
            case 1:
                listar()
            case 2:
                adicionar()
            case 3:
                editar()
            case 4:
                deletar()
            case 5:
                break