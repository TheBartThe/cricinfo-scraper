import pandas as pd

df = pd.read_csv("./data/batters.csv")
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
print(df)