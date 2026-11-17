def consultaCsv(tabela: str) -> list:
    valores = []#lista que será retornada com os valores retirados do arquivo csv.
    table = tabela + '.csv'#monta o nome do arquivo csv que será buscado

    #le linha por linha do arquivo csv e os adiciona na lista valores que será retornada.
    with open(table, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            valor = linha.strip()
            if valor == 'None':
                valores.append(None)
            elif valor == 'False':
                valores.append(False)
            elif valor == 'True':
                valores.append(True)
            elif valor.isdigit():
                valores.append(int(valor))
            else:
                valores.append(valor)

    return valores
