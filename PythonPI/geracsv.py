def geraCsv(tabela: str, valor: dict) -> None:
    table = tabela + ".csv"#monta o nome do arquivo csv que será gerado.
    valores = ""#variavel para guardar o que será escrito no arquivo csv.

    for item in valor.values():#coloca os valores que vinheram do create na variavel valores, sendo um valor por linha.
        valores += str(item) + '\n'
    with open(table, 'w', encoding='utf-8') as arquivo:
        arquivo.write(valores)#escreve o que o usuario forneceu no arquivo csv.