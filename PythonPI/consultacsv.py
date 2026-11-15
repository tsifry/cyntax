def consultaCsv(tabela):
    valores = []
    table = tabela + '.csv'

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
