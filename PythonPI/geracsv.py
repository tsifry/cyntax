def geraCsv(tabela, valor):
    table = tabela + ".csv"
    valores = ""
    for item in valor.values():
        valores += str(item) + '\n'
    with open(table, 'w', encoding='utf-8') as arquivo:
        arquivo.write(valores)