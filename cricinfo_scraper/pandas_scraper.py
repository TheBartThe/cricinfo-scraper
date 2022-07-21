"""
Collects data from a cricinfo scorecard and outputs it into a csv

Functions:

    read_scorecard(str) -> DataFrame
"""

import pandas as pd
from pandas import DataFrame
from typing import List


def read_scorecard(link: str):
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
