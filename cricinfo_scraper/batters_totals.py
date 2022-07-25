"""
Creates a dataframe with the totals for each batter

Functions:

    batters_totals(DataFrame) -> DataFrame
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
