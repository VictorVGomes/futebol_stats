import os.path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title="futstats")


from src.stats.stats import *
from src.utils.futils import *
from src.utils.useful_strings import *

tabs_names = useful_strings["tabs_names"]
tabs = st.tabs(tabs_names)
df = None

if "usar_todos_os_anos" not in st.session_state:
    st.session_state.usar_todos_os_anos = True

if "usar_todos_os_anos_tab4" not in st.session_state:
    st.session_state.usar_todos_os_anos_tab4 = True

with tabs[0]:
    left_column_tab0, right_column_tab0 = st.columns(2)

    with left_column_tab0:
        st.title("""FutStats""")
        st.markdown(useful_strings["futstatsInfo"])

        uploaded_file = st.file_uploader(useful_strings["fUploaderText"])
        usar_base_padrao = st.checkbox(
            useful_strings["basePadrao"], key="basePadrao"
        )
        caminhoDeArquivo = st.text_input(
            useful_strings["indique"], useful_strings["fakePath"]
        )

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

        elif usar_base_padrao:
            df = loadData(useful_strings["basePadraofPath"])

        elif not text_box_filled(caminhoDeArquivo, useful_strings["fakePath"]):
            if os.path.isfile(caminhoDeArquivo):
                df = pd.read_csv(caminhoDeArquivo)

            else:
                st.warning(
                    """O caminho dado não é válido! Verifique a escrita."""
                )

    if df is not None:
        df["ano_campeonato"] = df["ano_campeonato"].map(str)
        variaveis = df.columns[df.dtypes != "O"].tolist()

        with right_column_tab0:
            st.title("""Visão geral da base de dados""")
            st.dataframe(df, height=465)

if df is not None:
    all_vars = list(df.columns)
    variaveis = [
        v
        for v in variaveis
        if any(
            [
                i in v
                for i in [
                    "gol",
                    "escanteio",
                    "falta",
                    "chute",
                    "defesa",
                    "impedimento",
                ]
            ]
        )
    ]

    with tabs[1]:
        st.title(tabs_names[1])
        left_column_tab1, right_column_tab1 = st.columns(2)

        with left_column_tab1:
            var1 = st.selectbox(
                "Variáveis disponíveis", variaveis, key="lctab1"
            )
            var1name = " ".join(var1.split("_"))
            p1 = px.histogram(
                df,
                var1,
                nbins=8,
                text_auto=True,
                histfunc="count",
                title=f"{var1name}",
            )
            st.plotly_chart(p1)

            st.write(f"Estatísticas sumárias de {var1name}:")
            descr_var1 = df[var1].describe().values.reshape(1, -1)
            descr_var1 = pd.DataFrame(descr_var1, columns=descriptive_cols)
            st.dataframe(descr_var1, hide_index=True)

        with right_column_tab1:
            var2 = st.selectbox(
                "Variáveis disponíveis", variaveis, key="rctab1"
            )
            var2name = " ".join(var2.split("_"))
            p2 = px.histogram(
                df,
                var2,
                nbins=8,
                text_auto=True,
                histfunc="count",
                title=var2name,
            )
            st.plotly_chart(p2)

            st.write(f"Estatísticas sumárias de {var2name}:")
            descr_var2 = describe_(df=df, col=var2)
            st.dataframe(descr_var2, hide_index=True)

        with left_column_tab1:
            pass

    # A tab 1 vai ser feita de instruções pra gerar uma
    # base de dados no mesmo formato, contendo as mesmas colunas
    # TAB 2
    with tabs[2]:
        left_column_tab2, right_column_tab2 = st.columns(2)

        with left_column_tab2:
            times_disponiveis = list(
                set(df["time_mandante"].unique().tolist()).union(
                    set(df["time_visitante"].unique().tolist())
                )
            )

            st.markdown(f"### {tabs_names[2]}")
            time_selecionado = st.selectbox(
                "Times disponíveis", times_disponiveis
            )

            jogosEm = st.radio(
                "Juntar estatísticas sobre jogos:",
                ["Fora", "Em casa", "Fora e em casa"],
                captions=[
                    "Apenas jogos fora",
                    "Apenas jogos em casa",
                    "Estatísticas de ambos",
                ],
                horizontal=True,
                key="tab2",
            )

            anos_filtro = st.multiselect(
                "Juntar estatísticas sobre jogos nos anos:",
                df["ano_campeonato"].unique().tolist(),
                key="ms1",
                disabled=st.session_state.usar_todos_os_anos,
            )
            usar_todos_os_anos = st.checkbox(
                "Usar todos os anos disponíveis",
                key="usar_todos_os_anos",
                value=True,
            )

            conforto = (
                "mandante"
                if jogosEm == "Em casa"
                else ("visitante" if jogosEm == "Fora" else "ambos")
            )

            dfanos = get_years(df, anos_filtro, usar_todos_os_anos)

            if conforto != "ambos":
                # dados do time
                dados_time = describe_(
                    col=f"gols_{conforto}",
                    filter=(f"time_{conforto}", time_selecionado),
                    df=dfanos,
                )
                total_gols = get_total_goals_from_team(
                    dfanos, time_selecionado, conforto
                )
                # dados contra o time
                complementar_conforto = (
                    "visitante" if conforto == "mandante" else "mandante"
                )

                dados_contra_time = describe_(
                    col=f"gols_{complementar_conforto}",
                    filter=(f"time_{conforto}", time_selecionado),
                    df=dfanos,
                )
                total_gols_contra_time = get_total_goals_vs_team(
                    dfanos, time_selecionado, conforto, complementar_conforto
                )

            else:
                dados_time = get_all_data_from_team(
                    team=time_selecionado,
                    team_columns=["time_mandante", "time_visitante"],
                    correct_cols=[
                        ("gols_mandante", "gols_do_time"),
                        ("gols_visitante", "gols_do_time"),
                    ],
                    df=dfanos,
                )
                total_gols = dados_time["gols_do_time"].sum()
                dados_time = describe_(df=dados_time, col="gols_do_time")

                dados_contra_time = get_all_data_from_team(
                    team=time_selecionado,
                    team_columns=["time_mandante", "time_visitante"],
                    correct_cols=[
                        ("gols_visitante", "gols_contra_time"),
                        ("gols_mandante", "gols_contra_time"),
                    ],
                    df=dfanos,
                )
                total_gols_contra_time = dados_contra_time[
                    "gols_contra_time"
                ].sum()
                dados_contra_time = describe_(
                    df=dados_contra_time, col="gols_contra_time"
                )

            dados_time["total_gols"] = total_gols

            dados_contra_time[
                f"gols_vs_{time_selecionado}"
            ] = total_gols_contra_time

            st.write(
                f"""#### Estatísticas descritivas de gols da/do {time_selecionado}"""
            )
            st.write(
                f"Como a/o {time_selecionado} se sai contra outros times, no geral?"
            )
            st.dataframe(dados_time, width=700, hide_index=True)

            st.write(
                f"""#### Estatísticas descritivas de gols contra a/o {time_selecionado}"""
            )
            st.write(
                f"Como os times se saem contra a/o {time_selecionado}, no geral?"
            )
            st.dataframe(dados_contra_time, width=700, hide_index=True)

        with right_column_tab2:
            st.markdown(
                f"### Times que se saem pior contra a/o {time_selecionado}"
            )

            if conforto == "ambos":
                dfanalise = get_all_data_from_team_(dfanos, time_selecionado)
            else:
                dfanalise = filter_one(dfanos, time_selecionado, conforto)

            dfanalise = add_winners_stats_columns(dfanalise, time_selecionado)

            vs_outros_times = (
                dfanalise.groupby("oponente")
                .agg(
                    {
                        f"{time_selecionado}_vence": "mean",
                        f"gols_{time_selecionado}": "mean",
                        "gols_outro_time": "mean",
                        "gols_visitante": "count",
                        "empate": "mean",
                    }
                )
                .sort_values(by=f"{time_selecionado}_vence", ascending=False)
            )

            vs_outros_times = vs_outros_times.rename(
                columns={
                    f"{time_selecionado}_vence": f"{time_selecionado}_vence (%)",
                    f"gols_{time_selecionado}": f"media_gols_{time_selecionado}",
                    "gols_outro_time": "media_gols_outro_time",
                    "gols_visitante": "jogos_vs_outro_time",
                    "empate": "empates (%)",
                }
            )
            vs_outros_times[f"{time_selecionado}_vence (%)"] *= 100
            vs_outros_times["empates (%)"] *= 100

            st.dataframe(vs_outros_times, height=700)

    # TAB 3
    with tabs[3]:
        st.write(f"## Estatísticas para a/o {time_selecionado}")
        st.write("##### Escolha as variáveis para os gráficos e estatísticas:")
        if conforto == "ambos":
            dados_time_ = get_all_data_from_team(
                df=df,
                team=time_selecionado,
                team_columns=["time_mandante", "time_visitante"],
                correct_cols=[
                    ("gols_mandante", "gols_do_time"),
                    ("gols_visitante", "gols_do_time"),
                ],
            )
        else:
            dados_time_ = get_data_from_team(
                df=df, team=time_selecionado, comfort=f"time_{conforto}"
            )

        cont1 = st.container()
        with cont1:
            c1rt3, c1lt3 = st.columns(2)
            with c1rt3:
                var3 = st.selectbox(
                    "Variáveis eixo X", variaveis, key="rctab21"
                )
                var4 = st.selectbox(
                    "Variáveis eixo Y", variaveis, key="rctab22", index=3
                )
            with c1lt3:
                var5 = st.selectbox(
                    "Variáveis eixo Z",
                    ["-"] + variaveis,
                    key="rctab23",
                    index=None,
                )
                var6 = st.selectbox(
                    "Selecione uma variável de agrupamento:",
                    ["-"] + team_specific_grouping_variables,
                    key="rctab24",
                )

        var3name = " ".join(var3.split("_"))
        var4name = " ".join(var4.split("_"))

        if var5 == "-" or var5 is None:
            p3 = px.scatter(
                dados_time_,
                var3,
                var4,
                color=None if var6 == "-" else var6,
                title=f"{var3name} vs {var4name}",
            )
            p3.update_traces(
                marker=dict(
                    size=12, line=dict(width=2, color="DarkSlateGrey")
                ),
                selector=dict(mode="markers"),
            )

        else:
            var5name = " ".join(var5.split("_"))
            p3 = px.scatter_3d(
                dados_time_,
                var3,
                var4,
                var5,
                color=None if var6 == "-" else var6,
                title=f"{var3name} vs {var4name} vs {var5name}",
                symbol=None if var6 == "-" else var6,
            )
            p3.update_traces(
                marker=dict(size=8, line=dict(width=2, color="DarkSlateGrey")),
                selector=dict(mode="markers"),
            )
            p3.update_layout(margin=dict(l=0, r=0, b=0, t=25))

        st.plotly_chart(p3, use_container_width=True)

        cont2 = st.container()

        with cont2:
            lcont, rcont = st.columns(2)
            with lcont:
                st.write(f"Estatísticas sumárias de {var3name}:")
                descr_var3 = describe_(dados_time_, var3)
                st.dataframe(descr_var3, hide_index=True)

                if var5 != "-" and var5 is not None:
                    st.write(f"Estatísticas sumárias de {var5name}:")
                    descr_var5 = describe_(dados_time_, var5)
                    st.dataframe(descr_var5, hide_index=True)

            with rcont:
                st.write(f"Estatísticas sumárias de {var4name}:")
                descr_var4 = describe_(dados_time_, var4)
                st.dataframe(descr_var4, hide_index=True)

    # TAB 4
    with tabs[4]:
        if "time_A" not in st.session_state:
            st.session_state.time_A, st.session_state.time_B = "A", "B"

        tab4_container1 = st.container()

        with tab4_container1:
            t4c1l1, t4c1r1, t4c1r2 = st.columns(3)

            with t4c1l1:
                st.session_state.time_A = st.selectbox(
                    "Selecione o time A",
                    df["time_mandante"].unique().tolist(),
                    key="t4c1l1",
                )
            with t4c1r2:
                st.session_state.time_B = st.selectbox(
                    "Selecione o time B",
                    df["time_mandante"].unique().tolist(),
                    key="t4c1r1",
                    index=3,
                )
            with t4c1r1:
                anos_filtro_tab4 = st.multiselect(
                    "Juntar estatísticas sobre jogos nos anos:",
                    df["ano_campeonato"].unique().tolist(),
                    key="ms_tab4",
                    disabled=st.session_state.usar_todos_os_anos_tab4,
                )
                usar_todos_os_anos_tab4 = st.checkbox(
                    "Usar todos os anos disponíveis",
                    key="usar_todos_os_anos_tab4",
                    value=True,
                )

        dfanos2 = get_years(df, anos_filtro_tab4, usar_todos_os_anos_tab4)
        tab4_container2 = st.container()

        with tab4_container2:
            t4c2l1, t4c2r1, t4c2r2 = st.columns(3)

            df_time_A = get_all_data_from_team_(
                dfanos2, st.session_state.time_A
            )

            df_time_A_B = get_all_data_from_team_(
                df_time_A, st.session_state.time_B
            )

            del df_time_A, dfanos2

            with t4c2r1:
                st.markdown(
                    f"## {st.session_state.time_A} vs {st.session_state.time_B}"
                )

            with t4c2l1:
                nJogos = df_time_A_B.shape[0]
                time_A_venceu = get_winner(
                    df_time_A_B, st.session_state.time_A
                )
                time_B_venceu = get_winner(
                    df_time_A_B, st.session_state.time_B
                )

            with t4c2l1:
                st.markdown(
                    f"### Jogos em que o {st.session_state.time_A} venceu"
                )
                st.dataframe(
                    df_time_A_B.iloc[time_A_venceu, :],
                    height=300,
                    hide_index=True,
                )

            with t4c2r2:
                st.markdown(
                    f"### Jogos em que o {st.session_state.time_B} venceu"
                )
                st.dataframe(
                    df_time_A_B.iloc[time_B_venceu, :],
                    height=300,
                    hide_index=True,
                )

            gols_time_A_visit = get_goals(
                df_time_A_B, st.session_state.time_A, "visitante"
            )
            gols_time_A_mand = get_goals(
                df_time_A_B, st.session_state.time_A, "mandante"
            )
            gols_A_total = gols_time_A_visit + gols_time_A_mand

            gols_time_B_visit = get_goals(
                df_time_A_B, st.session_state.time_B, "visitante"
            )
            gols_time_B_mand = get_goals(
                df_time_A_B, st.session_state.time_B, "mandante"
            )
            gols_B_total = gols_time_B_visit + gols_time_B_mand

            with t4c2r1:
                st.markdown(f"#### Num total de {nJogos} jogos:")
                st.markdown(
                    f"###### a/o :green[{st.session_state.time_A} venceu {(A_venceu := len(time_A_venceu))}] ({(A_venceu / nJogos * 100 if nJogos > 0 else 0):.2f}%) jogos do/a {st.session_state.time_B}"
                )
                st.markdown(
                    f"###### a/o :green[{st.session_state.time_B} venceu {(B_venceu := len(time_B_venceu))}] ({(B_venceu / nJogos * 100 if nJogos > 0 else 0):.2f}%) jogos do/a {st.session_state.time_A}"
                )
                st.markdown(
                    f"""###### :blue[{(empates_AB := nJogos - (A_venceu + B_venceu))} empate{'s ocorreram' if empates_AB!=1 else ' ocorreu'} ({(empates_AB / nJogos * 100 if nJogos > 0 else 0):.2f}%) no período selecionado.]"""
                )
                st.markdown(
                    f"""###### O {st.session_state.time_A} marcou {gols_A_total} gols contra o {st.session_state.time_B}, sendo {gols_time_A_visit} ({(gols_time_A_visit / gols_A_total * 100 if nJogos > 0 else 0):.2f}%) deles fora de casa e {gols_time_A_mand} ({(gols_time_A_mand / gols_A_total * 100 if gols_A_total > 0 else 0):.2f}%) em casa."""
                )

                st.markdown(
                    f"""###### O {st.session_state.time_B} marcou {gols_B_total} gols contra o {st.session_state.time_A}, sendo {gols_time_B_visit} ({(gols_time_B_visit / gols_B_total * 100 if nJogos > 0 else 0):.2f}%) deles fora de casa e {gols_time_B_mand} ({(gols_time_B_mand / gols_B_total * 100 if gols_B_total > 0 else 0):.2f}%) em casa."""
                )

        st.divider()
        st.title(
            f"Estatísticas Descritivas: {st.session_state.time_A} vs {st.session_state.time_B}"
        )
        var_tab4 = st.selectbox(
            "Escolha uma variável para analisar:",
            variaveis,
            key="tab4_select_n",
        )
        tab4_container3 = st.container()
        with tab4_container3:
            t4c3l1, t4c3r1 = st.columns(2)

            with t4c3l1:
                descr_time_A_visit = df_time_A_B[
                    df_time_A_B["time_visitante"] == st.session_state.time_A
                ]
                descr_time_A_visit = describe_(descr_time_A_visit, var_tab4)
                st.markdown(
                    f"#### {var_tab4} com {st.session_state.time_A} visitante"
                )
                st.dataframe(descr_time_A_visit, hide_index=True)

                descr_time_A_mand = df_time_A_B[
                    df_time_A_B["time_mandante"] == st.session_state.time_A
                ]
                descr_time_A_mand = describe_(descr_time_A_mand, var_tab4)
                st.markdown(
                    f"#### {var_tab4} com {st.session_state.time_A} mandante"
                )
                st.dataframe(descr_time_A_mand, hide_index=True)

            with t4c3r1:
                descr_time_B_visit = df_time_A_B[
                    df_time_A_B["time_visitante"] == st.session_state.time_B
                ]
                descr_time_B_visit = describe_(descr_time_B_visit, var_tab4)
                st.markdown(
                    f"#### {var_tab4} com {st.session_state.time_B} visitante"
                )
                st.dataframe(descr_time_B_visit, hide_index=True)

                descr_time_B_mand = df_time_A_B[
                    df_time_A_B["time_mandante"] == st.session_state.time_B
                ]
                descr_time_B_mand = describe_(descr_time_B_mand, var_tab4)
                st.markdown(
                    f"#### {var_tab4} com {st.session_state.time_B} mandante"
                )
                st.dataframe(descr_time_B_mand, hide_index=True)
