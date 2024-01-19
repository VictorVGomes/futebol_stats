import os
import streamlit as st
import pandas as pd


def _isfile(filename: str) -> bool:
    """Checks if a certain file exists in a given directory

    Args:
        filename (str): the path/name of the file

    Returns:
        bool: True if the file exists, False otherwise
    """
    return os.path.isfile(filename)


def fname_to_csvname(filename: str) -> str:
    """checks if the filename ends with .csv,
       if it doesn't, make expected corrections
       and return the right filename.

    Args:
        filename (str): filename to be checked

    Returns:
        str: corrected filename
    """
    filename = f"{filename.split('.')[0]}.csv" if not filename.endswith(".csv") else filename
    return filename


def makefile(filename: str) -> None:
    """creates a .csv file with the given filename, if it doesn't already exist.

    Args:
        filename (str): the name of the file
    """
    filename = fname_to_csvname(filename)

    if not _isfile(filename):
        with open(filename, "w") as f:
            f.write("")


@st.cache_data
def loadData(filename: str) -> pd.core.frame.DataFrame:
    """loads the data of the given .csv filename if it exists

    Args:
        filename (str): path containing the name of the file to be read

    Returns:
        pd.core.frame.DataFrame: loaded data
    """
    filename = fname_to_csvname(filename)

    if _isfile(filename=filename):
        df = pd.read_csv(filename)
        return df


def text_box_filled(text: str, not_filled_text: str) -> bool:
    """checks if the not_filled_text is in the main text

    Args:
        text (str): main text
        not_filled_text (str): check

    Returns:
        bool: True if not_filled_text in text, False otherwise
    """
    return not_filled_text in text
