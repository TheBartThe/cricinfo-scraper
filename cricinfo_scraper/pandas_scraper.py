"""
Collects data from a cricinfo scorecard and outputs it into a csv

Functions:

    read_scorecard(str) -> DataFrame
    get_all_scorecards(List[str]) -> DataFrame
    store_raw_scorecard(List[str]) -> None
"""

from typing import List
import pandas as pd
from pandas import DataFrame


def read_scorecard(link: str) -> DataFrame:
    """
    Reads a table of batting info from a cricinfo scorecard link, and return a pandas dataframe

            Parameters:
                link (str): url link to a cricinfo scorecard

            Returns:
                df (DataFrame): dataframe containing raw data of batting scorecards
    """

    tables: List[DataFrame] = pd.read_html(link, match="BATTING")
    df: DataFrame = pd.concat(tables)
    return df


def get_all_scorecards(links: List[str]) -> DataFrame:
    """
    Reads tables of batting info from a list of cricinfo scorecard links, and return a pandas dataframe

            Parameters:
                links (List[str]): url link to cricinfo scorecards

            Returns:
                df (DataFrame): dataframe containing raw data of batting scorecards
    """
    frames: List[DataFrame] = [read_scorecard(link) for link in links]
    df: DataFrame = pd.concat(frames)
    return df


def store_raw_scorecard(links: List[str]) -> None:
    """
    Reads tables of batting info from a list of cricinfo scorecard links, and stores them in a csv file

            Parameters:
                links (List[str]): url link to cricinfo scorecards

            Returns:
                None
    """
    df = get_all_scorecards(links)
    df.to_csv("./data/batters.csv")
