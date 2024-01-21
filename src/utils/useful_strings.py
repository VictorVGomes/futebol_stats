useful_strings = dict(
    tabs_names=[
        "Início",
        "Estatísticas gerais",
        "Estatísticas por time (Em casa (mandante)/Fora (Visitante)/Ambos)",
        "Estatísticas por time (Em casa (mandante)/Fora (Visitante)/Ambos) - gráficos",
        "Time A vs Time B",
    ],
    futstatsInfo="""
Um App simples para fazer análises relacionadas a futebol (apesar de funcionar para outros contextos).
Existem 3 formas de iniciar as análises:

1. Adicionar uma base de dados no formato .csv usando o **uploader** de arquivos abaixo
2. **Cheque** a caixa "Usar base padrão", para usar a base padrão
3. ou indique o caminho até o arquivo .csv a ser lido
    

Caso as 3 opções sejam indicadas ao mesmo tempo, a ordem de uso será como a numeração dada acima.
                    
    """,
    fUploaderText="""Selecione um arquivo no formato '<seu_arquivo>.csv'""",
    basePadrao="Usar base padrão (Brasileirão série A)",
    basePadraofPath="src/datasets/brasileirao_serie_a",
    fakePath="""Ex.: C:/Users/<seu_user>/Área de Trabalho/brasileirao.csv""",
    indique="Indique o caminho até o seu arquivo:",
)

columns_to_keep = [""]

descriptive_cols = [
    "# de jogos",
    "Média",
    "Desvio-padrão",
    "Mín.",
    "25%",
    "50% (Mediana)",
    "75%",
    "Máx.",
]
team_specific_grouping_variables = [
    "ano_campeonato",
    "estadio",
    "rodada",
    "tecnico_mandante",
    "tecnico_visitante",
    "colocacao_mandante",
    "colocacao_visitante",
    "arbitro",
]
