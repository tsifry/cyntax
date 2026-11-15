from tabelas import TABELAS

def criatabelas(conexao):
    cursor = conexao.cursor()

    #1TABELA USUARIOS
    sql = """
    CREATE TABLE IF NOT EXISTS Usuarios (
    ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    EMAIL VARCHAR(255) NOT NULL UNIQUE,
    NOME VARCHAR(255) NOT NULL,
    FOTO_PERFIL TEXT NULL,
    ASSINANTE BOOLEAN NOT NULL DEFAULT FALSE
    )
    """
    cursor.execute(sql)

    #2TABELA AUTENTICACAO
    sql = """
        CREATE TABLE IF NOT EXISTS Autenticacao (
        ID BIGINT PRIMARY KEY AUTO_INCREMENT,
        ID_USUARIO BIGINT NOT NULL,
        SENHA VARCHAR(255) NOT NULL,
        FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(ID)
        )
        """
    cursor.execute(sql)

    #3TABELA Módulos
    sql = """
        CREATE TABLE IF NOT EXISTS Modulos (
        ID BIGINT PRIMARY KEY AUTO_INCREMENT,
        NOME VARCHAR(150) NOT NULL,
        DIFICULDADE VARCHAR(30) NOT NULL,
        ASSINANTE BOOLEAN NOT NULL DEFAULT FALSE
        )
        """
    cursor.execute(sql)

    #4TABELA PROBLEMASaqui teria o resposta
    sql = """
        CREATE TABLE IF NOT EXISTS Problemas (
        ID BIGINT PRIMARY KEY AUTO_INCREMENT,
        ID_MODULO BIGINT,
        DESCRICAO TEXT NOT NULL,
        FOREIGN KEY (ID_MODULO) REFERENCES Modulos(ID)
        )
        """
    cursor.execute(sql)

    #5TABELA JOGOS
    sql = """
        CREATE TABLE IF NOT EXISTS Jogos (
        ID BIGINT PRIMARY KEY AUTO_INCREMENT,
        ID_MODULO BIGINT,
        DESCRICAO TEXT NOT NULL,
        SANDBOX BOOLEAN NOT NULL,
        FOREIGN KEY (ID_MODULO) REFERENCES Modulos(ID)
        )
        """
    cursor.execute(sql)

#6TABELA PROGRESSOPROBLEMAS
    sql = """
        CREATE TABLE IF NOT EXISTS ProgressoProblemas (
        ID_PROBLEMA BIGINT,
        ID_USUARIO BIGINT NOT NULL,
        TENT_TOTAIS INTEGER NOT NULL,
        FINALIZADO BOOLEAN NOT NULL DEFAULT FALSE,
        TEMPO_GASTO BIGINT NOT NULL DEFAULT 0,
        FOREIGN KEY (ID_PROBLEMA) REFERENCES Problemas(ID),
        FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(ID)
        )
        """
    cursor.execute(sql)

#7TABELA PROGRESSOJOGOS
    sql = """
        CREATE TABLE IF NOT EXISTS ProgressoJogos (
        ID_JOGO BIGINT NOT NULL,
        ID_USUARIO BIGINT NOT NULL,
        JOGADOS INTEGER NOT NULL DEFAULT 0,
        HIGHSCORE INTEGER NOT NULL DEFAULT 0,
        TEMPO_JOGADO BIGINT NOT NULL DEFAULT 0,
        FOREIGN KEY (ID_JOGO) REFERENCES Jogos(ID),
        FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(ID)
        )
        """
    cursor.execute(sql)

#8TABELA PONTUACAOHISTORICO
    sql = """
        CREATE TABLE IF NOT EXISTS PontuacaoHistorico (
        ID BIGINT AUTO_INCREMENT PRIMARY KEY, 
        ID_USUARIO BIGINT NOT NULL,
        TIPO_ATIVIDADE VARCHAR(20) NOT NULL,
        ID_ATIVIDADE BIGINT NOT NULL,
        PONTUACAO INTEGER NOT NULL,
        DATA_CONQ TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        TEMPORADA TINYINT NOT NULL,
        FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(ID)
        )
        """
    cursor.execute(sql)

#9TABELA RANKING
    sql = """
        CREATE TABLE IF NOT EXISTS Ranking ( 
        ID_USUARIO BIGINT NOT NULL,
        COLOCACAO INTEGER NULL,
        PONTUACAO BIGINT NOT NULL DEFAULT 0,
        TEMPORADA TINYINT NOT NULL,
        FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(ID)
        )
        """
    cursor.execute(sql)




