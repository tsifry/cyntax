import mysql.connector

def conecta():
    conexao = mysql.connector.connect(
    host="srv1545.hstgr.io",
    user="u704608208_turma_manha",
    password="2845@fatecSCS",
    database="u704608208_turma_manha"
    )

    return conexao