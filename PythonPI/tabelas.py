TABELAS = {
    "Usuarios": [
        ("ID", int, "AUTO"),
        ("EMAIL", str, "NOT_NULL"),
        ("NOME", str, "NOT_NULL"),
        ("FOTO_PERFIL", str, "NULL"),
        ("ASSINANTE", bool, "DEFAULT")
    ],

    "Autenticacao": [
        ("ID", int, "AUTO"),
        ("ID_USUARIO", int, "NOT_NULL"),
        ("SENHA", str, "NOT_NULL")
    ],

    "Modulos": [
            ("ID", int, "AUTO"),
            ("NOME", str, "NOT_NULL"),
            ("DIFICULDADE", str, "NOT_NULL"),
            ("ASSINANTE", bool, "DEFAULT")
        ],

    "Problemas": [
                ("ID", int, "AUTO"),
                ("ID_MODULO", int, "NOT_NULL"),#fk
                ("DESCRICAO", str, "NOT_NULL")
                #("RESPOSTA", , )
            ],

    "Jogos": [
        ("ID", int, "AUTO"),
        ("ID_MODULO", int, "NOT_NULL"),#fk
        ("DESCRICAO", str, "NOT_NULL"),
        ("SANDBOX", bool, "NOT_NULL")
    ],

    "ProgressoProblemas": [
            ("ID_PROBLEMA", int, "NOT_NULL"),#fk
            ("ID_USUARIO", int, "NOT_NULL"),#fk
            ("TENT_TOTAIS", int, "NOT_NULL"),
            ("FINALIZADO", bool, "DEFAULT"),
            ("TEMPO_GASTO", int, "DEFAULT")
        ],

    "ProgressoJogos": [
                ("ID_JOGO", int, "NOT_NULL"),#fk
                ("ID_USUARIO", int, "NOT_NULL"),#fk
                ("JOGADOS", int, "DEFAULT"),
                ("HIGHSCORE", int, "DEFAULT"),
                ("TEMPO_JOGADO", int, "DEFAULT")
            ],

    "PontuacaoHistorico": [
                    ("ID", int, "AUTO"),
                    ("ID_USUARIO", int, "NOT_NULL"),#fk
                    ("TIPO_ATIVIDADE", str, "NOT_NULL"),
                    ("ID_ATIVIDADE", int, "NOT_NULL"),
                    ("PONTUACAO", int, "NOT_NULL"),
                    ("DATA_CONQ", str, "NOT_NULL"),#coloquei str pq o tipo timestamp é pra contar seg ou miliseg desde um tempo especifico
                    ("TEMPORADA", int, "NOT_NULL")
                ],

    "Ranking": [
                    ("ID_USUARIO", int, "NOT_NULL"),#fk
                    ("COLOCACAO", int, "NULL"),
                    ("PONTUACAO", int, "DEFAULT"),
                    ("TEMPORADA", int, "NOT_NULL")
                ]
}