"""
Collects data from a cricinfo scorecard and outputs it into a csv
"""

import pandas as pd

tables = pd.read_html("https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/gujarat-titans-vs-rajasthan-royals-final-1312200/full-scorecard", match="BATTING")
df = pd.concat(tables)
df.to_csv("./data/batters.csv")
