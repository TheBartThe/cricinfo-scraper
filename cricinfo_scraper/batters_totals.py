"""
Creates a dataframe with the totals for each batter

Functions:

    batters_totals(DataFrame) -> DataFrame
    store_batters_totals() -> None
"""


import pandas as pd
from pandas import DataFrame


def batters_totals(df: DataFrame) -> DataFrame:
    """
    Returns a dataframe of each batters totals

            Parameters:
                    df (DataFrame): A cleaned dataframe of batters from a scorecard

            Returns:
                    totals_df (DataFrame): A dataframe with the totals for each batter
    """
    totals_df: DataFrame = df.groupby("Batter", as_index=False)[
        ["Runs", "Balls", "Minutes", "Fours", "Sixes", "Out"]
    ].sum()
    return totals_df


def store_batters_totals() -> None:
    """
    Stores a dataframe of each batters totals as a csv file

            Parameters:
                    None

            Returns:
                    None
    """
    df = pd.read_csv("./data/batters_cleaned.csv")
    df = batters_totals(df)
    df.to_csv("./data/batters_totals.csv")
