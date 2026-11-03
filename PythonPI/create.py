def create(conexao):
    cursor = conexao.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS alunosPI (
    id INT PRIMARY KEY AUTO_INCREMENT,
    matricula INT,
    nome VARCHAR(100),
    idade INT
    )
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO alunosPI (nome, idade)
    VALUES (%s, %s)
    """
    campo1 = input('Digite o nome do aluno: ')
    campo2 = int(input('Digite a idade do aluno: '))
    
    cursor.execute(sql, (campo1, campo2))
    conexao.commit()

    cursor.close()