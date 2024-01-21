import pandas as pd
import streamlit as st
import numpy as np

aggregation_dict = dict(
    mediana="median",
    variancia="var",
    media="mean",
    desvio="std",
    maximo="max",
    minimo="min",
    min="min",
    max="max",
    soma="sum",
    var="var",
)
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


def get_data_from_team(
    df: pd.DataFrame, team: str, comfort: str
) -> pd.DataFrame:
    df = df.copy(deep=True)
    return df[df[comfort] == team]


def get_column_aggregation(
    df: pd.DataFrame,
    column: str,
    aggr: str,
    filter: (tuple or None) = None,
    group: str or None = None,
) -> pd.core.frame.DataFrame or float:
    (key, value) = filter
    df = df.copy(deep=True)
    df = df[df[key] == value] if filter is not None else df

    aggr = aggregation_dict.get(aggr, "mean")

    if group is not None:
        df = df.groupby(group)
        agg = df.agg({column: aggr}).reset_index()
    else:
        agg = df.agg({column: aggr})

    return agg


@st.cache_data
def get_all_data_from_team(
    df: pd.DataFrame,
    team: str,
    team_columns: list,
    correct_cols: list or None = None,
):
    df = df.copy(deep=True)
    data = []

    for idx, col in enumerate(team_columns):
        filtered_data = df[df[col] == team].copy(deep=True)

        if correct_cols is not None:
            (old_col, new_col) = correct_cols[idx]
            filtered_data.loc[:, new_col] = filtered_data[old_col]

        data.append(filtered_data)

    gathered_data = pd.concat(data)
    return gathered_data


@st.cache_data
def describe_(
    df: pd.DataFrame, col: str, filter: tuple = None
) -> pd.DataFrame:
    """Describes (in statistical terms) the chosen variable of a dataframe

    Args:
        col (str): which variable to describe
        filter (tuple): will any filters be applied
        df (pd.DataFrame, optional): the dataframe to be used. if None, will use self.df.
        Defaults to None.

    Returns:
        pd.DataFrame: described variable from the data
    """
    df = df.copy(deep=True)

    if filter is not None:
        (filter_col, cat) = filter
        df = df[df[filter_col] == cat]

    descr = df[col].describe().round(2)
    if len(descr.shape) < 2:
        descr = descr.values.reshape(1, -1)
    descr = pd.DataFrame(descr, columns=descriptive_cols)

    return descr


def get_years(df: pd.DataFrame, years: list, use_all: bool):
    df_from_years = (
        df[df["ano_campeonato"].isin(years)]
        if not use_all
        else df.copy(deep=True)
    )
    return df_from_years


def get_total_goals_from_team(
    df: pd.DataFrame,
    team: str,
    comfort: str,
) -> int:
    return int(df[df[(f"time_{comfort}")] == team][f"gols_{comfort}"].sum())


def get_total_goals_vs_team(
    df: pd.DataFrame, team: str, comfort: str, counter_comfort: str
) -> int:
    return int(
        df[df[f"time_{comfort}"] == team][f"gols_{counter_comfort}"].sum()
    )


def get_all_data_from_team_(
    df,
    team,
) -> pd.DataFrame:
    return df[
        (df["time_visitante"] == team) | (df["time_mandante"] == team)
    ].reset_index(drop=True)


def filter_one(df, team, which) -> pd.DataFrame:
    return df[df[f"time_{which}"] == team].reset_index(drop=True)


def add_winners_stats_columns(df, team) -> pd.DataFrame:
    df = df.copy(deep=True)
    visit_vencedor = np.where(
        df["gols_visitante"] > df["gols_mandante"],
    )[0]
    mand_vencedor = np.where(
        df["gols_mandante"] > df["gols_visitante"],
    )[0]
    empates = np.where(
        df["gols_mandante"] == df["gols_visitante"],
    )[0]

    df["oponente"] = "-"
    df[f"gols_{team}"] = "-"
    df["gols_outro_time"] = "-"

    oponente_visitante = np.where(df["time_mandante"] == team)[0]
    oponente_mandante = np.where(df["time_visitante"] == team)[0]

    df.loc[oponente_visitante, "oponente"] = df.loc[
        oponente_visitante, "time_visitante"
    ]
    df.loc[oponente_mandante, "oponente"] = df.loc[
        oponente_mandante, "time_mandante"
    ]

    df.loc[oponente_visitante, f"gols_{team}"] = df.loc[
        oponente_visitante, "gols_mandante"
    ]
    df.loc[oponente_mandante, f"gols_{team}"] = df.loc[
        oponente_mandante, "gols_visitante"
    ]

    df.loc[oponente_visitante, f"gols_outro_time"] = df.loc[
        oponente_visitante, "gols_visitante"
    ]
    df.loc[oponente_mandante, f"gols_outro_time"] = df.loc[
        oponente_mandante, "gols_mandante"
    ]

    df["vencedor_confronto"] = "-"
    df.loc[visit_vencedor, "vencedor_confronto"] = df.loc[
        visit_vencedor, "time_visitante"
    ]
    df.loc[mand_vencedor, "vencedor_confronto"] = df.loc[
        mand_vencedor, "time_mandante"
    ]
    df.loc[empates, "vencedor_confronto"] = "empate"

    df[f"{team}_vence"] = df["vencedor_confronto"] == team
    df["empate"] = np.where(df["vencedor_confronto"] == "empate", 1, 0)

    return df


def get_winner(df, team) -> np.array:
    return np.where(
        (
            (df["time_visitante"] == team)
            & (df["gols_visitante"] > df["gols_mandante"])
        )
        | (
            (df["time_mandante"] == team)
            & (df["gols_mandante"] > df["gols_visitante"])
        )
    )[0]


def get_goals(df, team, comfort) -> int:
    return int(df[df[f"time_{comfort}"] == team][f"gols_{comfort}"].sum())
