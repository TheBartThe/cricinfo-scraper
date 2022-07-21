"""
Cleans the data from the scorecards collected from the cricinfo website

Functions:

    clean_batters_dataframe(DataFrame) -> DataFrame
"""

import pandas as pd
from pandas import DataFrame

#df: DataFrame = pd.read_csv("./data/batters.csv")

def clean_batters_dataframe(df: DataFrame) -> DataFrame:
    """
    Cleans and return a dataframe of batters.

            Parameters:
                    df (DataFrame): A dataframe of batters from a scorecard

            Returns:
                    df (DataFrame): A cleaned version of the input dataframe
    """
    df.drop(columns=["Unnamed: 0", "Unnamed: 8", "Unnamed: 9"], inplace=True)
    df.dropna(subset=["BATTING", "B"], inplace=True)
    df = df.loc[~df["BATTING"].str.startswith(("Did not bat", "Fall of wickets"))]
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={"BATTING": "Batting",
                    "Unnamed: 1": "Dismissal",
                    "R": "Runs",
                    "B": "Balls",
                    "M": "Minutes",
                    "SR": "StrikeRate"}, inplace=True)
    df["Out"] = df["Dismissal"] != "not out"
    df["Batting"] = df["Batting"].str.replace("(†|\(c\))","", regex=True).str.strip()
    return df
