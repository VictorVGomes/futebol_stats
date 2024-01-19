import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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


class stats_aggregator:
    """_summary_"""

    def __init__(self, df: pd.core.frame.DataFrame) -> None:
        """_summary_

        Args:
            df (pd.core.frame.DataFrame): _description_
        """
        self.df = df.copy(deep=True)
        self.columns = self.df.columns

    def get_data_from_team(self, team: str, comfort: str, df: pd.DataFrame = None) -> pd.DataFrame:
        df = self.df.copy(deep=True)
        return df[df[comfort] == team]

    def get_column_aggregation(
        self,
        column: str,
        aggr: str,
        filter: (tuple or None) = None,
        group: str or None = None,
        df: pd.DataFrame or None = None,
    ) -> pd.core.frame.DataFrame or float:
        """_summary_

        Args:
            column (str): _description_
            aggr (str): _description_
            filter (tuple or None, optional): _description_. Defaults to None.
            group (strorNone, optional): _description_. Defaults to None.
            df (pd.DataFrameorNone, optional): _description_. Defaults to None.

        Returns:
            pd.core.frame.DataFrame or float: _description_
        """
        (key, value) = filter
        df = self.df if df is None else df
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
        _self,
        team: str,
        team_columns: list,
        correct_cols: list or None = None,
        df: pd.DataFrame or None = None,
    ):
        """_summary_

        Args:
            team (str): which team
            team_columns (list): columns from which the team should be selected
            correct_cols (list or None, optional): . Defaults to None.

        Returns:
            _type_: _description_
        """
        df = _self.df if df is None else df
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
    def describe_(_self, col: str, filter: tuple, df: pd.DataFrame or None = None) -> pd.DataFrame:
        """Describes (in statistical terms) the chosen variable of a dataframe

        Args:
            col (str): which variable to describe
            filter (tuple): will any filters be applied
            df (pd.DataFrame, optional): the dataframe to be used. if None, will use self.df.
            Defaults to None.

        Returns:
            pd.DataFrame: described variable from the data
        """
        df = _self.df.copy(deep=True) if df is None else df
        (filter_col, cat) = filter
        if filter is not None:
            df = df[df[filter_col] == cat]
        return df[col].describe().round(2)


# def
