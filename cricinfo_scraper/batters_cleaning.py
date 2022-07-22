"""
Cleans the data from the scorecards collected from the cricinfo website

Functions:

    clean_batters_dataframe(DataFrame) -> DataFrame
    remove_unwanted_columns(DataFrame) -> DataFrame
    remove_unwanted_rows(DataFrame) -> DataFrame
    rename_columns(DataFrame) -> DataFrame
    clean_name(DataFrame) -> DataFrame
    out_column(DataFrame) -> DataFrame
    change_column_types(DataFrame) -> DataFrame
"""

import pandas as pd
from pandas import DataFrame

# df: DataFrame = pd.read_csv("./data/batters.csv", index_col = "Unnamed: 0")


def clean_batters_dataframe(df: DataFrame) -> DataFrame:
    """
    Cleans and return a dataframe of batters.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A cleaned version of the input dataframe
    """
    df = remove_unwanted_columns(df)
    df = remove_unwanted_rows(df)
    df = rename_columns(df)
    df = clean_name(df)
    df = out_column(df)
    return df


def remove_unwanted_columns(df: DataFrame) -> DataFrame:
    """
    Removes unwanted columns from a dataframe of batters.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters with unwanted columns removed
    """
    df.drop(columns=["Unnamed: 8", "Unnamed: 9"], inplace=True)
    return df


def remove_unwanted_rows(df: DataFrame) -> DataFrame:
    """
    Removes unwanted rows from a dataframe of batters.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters with unwanted rows removed
    """
    df.dropna(subset=["BATTING", "B"], inplace=True)
    df = df.loc[~df["BATTING"].str.startswith(("Did not bat", "Fall of wickets"))]
    df.reset_index(drop=True, inplace=True)
    return df


def rename_columns(df: DataFrame) -> DataFrame:
    """
    Renames columns in a dataframe of batters so they are consistent and more descriptive.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters with columns renamed
    """
    df.rename(
        columns={
            "BATTING": "Batter",
            "Unnamed: 1": "Dismissal",
            "R": "Runs",
            "B": "Balls",
            "M": "Minutes",
            "SR": "StrikeRate",
            "4s": "Fours",
            "6s": "Sixes",
        },
        inplace=True,
    )
    return df


def clean_name(df: DataFrame) -> DataFrame:
    """
    Cleans the name of the batter in the batters dataframe

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters with names cleaned
    """
    df["Batter"] = df["Batter"].str.replace("(†|\(c\))", "", regex=True).str.strip()
    return df


def out_column(df: DataFrame) -> DataFrame:
    """
    Adds a boolean column to the dataframe to indicate whether the batter was out.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters with out column added
    """
    df["Out"] = df["Dismissal"] != "not out"
    return df


def change_column_types(df: DataFrame) -> DataFrame:
    """
    Changes the column types to integers and a float where appropriate.

        Parameters:
                df (DataFrame): A dataframe of batters from a scorecard

        Returns:
                df (DataFrame): A dataframe of batters types corrected
    """
    df = df.astype(
        {
            "Runs": "int",
            "Balls": "int",
            "Minutes": "int",
            "Fours": "int",
            "Sixes": "int",
            "StrikeRate": "float",
        }
    )
    return df
