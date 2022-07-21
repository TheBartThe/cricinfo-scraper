"""
Collects data from a cricinfo scorecard and outputs it into a csv
"""

import pandas as pd


def read_scorecard(link: str):
    """
    Reads a table of batting info from a cricinfo scorecard link, and return a pandas dataframe

            Parameters:
                link (str): url link to a cricinfo scorecard

            Returns:
                df (pandas dataframe): dataframe containing raw data of batting scorecards
    """

    tables = pd.read_html(link, match="BATTING")
    df = pd.concat(tables)
    return df
