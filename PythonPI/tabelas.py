TABELAS = {
    "Usuarios": [
        ("ID", "AUTO"),
        ("EMAIL", "NOT_NULL"),
        ("NOME", "NOT_NULL"),
        ("FOTO_PERFIL", "NULL"),
        ("ASSINANTE", "DEFAULT")
    ],

    "Autenticacao": [
        ("ID", "AUTO"),
        ("ID_USUARIO", "NOT_NULL"),
        ("SENHA", "NOT_NULL")
    ],

    "Modulos": [
            ("ID", "AUTO"),
            ("NOME", "NOT_NULL"),
            ("DIFICULDADE", "NOT_NULL"),
            ("ASSINANTE", "DEFAULT")
        ],

    "Problemas": [
                ("ID", "AUTO"),
                ("ID_MODULO", "NOT_NULL"),#fk
                ("DESCRICAO", "NOT_NULL"),
                ("RESPOSTA", "NOT_NULL")
            ],

    "Jogos": [
        ("ID", "AUTO"),
        ("ID_MODULO", "NOT_NULL"),#fk
        ("DESCRICAO", "NOT_NULL"),
        ("SANDBOX", "NOT_NULL")
    ],

    "ProgressoProblemas": [
            ("ID_PROBLEMA", "NOT_NULL"),#fk
            ("ID_USUARIO", "NOT_NULL"),#fk
            ("TENT_TOTAIS", "NOT_NULL"),
            ("FINALIZADO", "DEFAULT"),
            ("TEMPO_GASTO", "DEFAULT")
        ],

    "ProgressoJogos": [
                ("ID_JOGO", "NOT_NULL"),#fk
                ("ID_USUARIO", "NOT_NULL"),#fk
                ("JOGADOS", "DEFAULT"),
                ("HIGHSCORE", "DEFAULT"),
                ("TEMPO_JOGADO", "DEFAULT")
            ],

    "PontuacaoHistorico": [
                    ("ID", "AUTO"),
                    ("ID_USUARIO", "NOT_NULL"),#fk
                    ("TIPO_ATIVIDADE", "NOT_NULL"),
                    ("ID_ATIVIDADE", "NOT_NULL"),
                    ("PONTUACAO", "NOT_NULL"),
                    ("DATA_CONQ", "NOT_NULL"),
                    ("TEMPORADA", "NOT_NULL")
                ],

    "Ranking": [
                    ("ID_USUARIO", "NOT_NULL"),#fk
                    ("COLOCACAO", "NULL"),
                    ("PONTUACAO", "DEFAULT"),
                    ("TEMPORADA", "NOT_NULL")
                ]
}