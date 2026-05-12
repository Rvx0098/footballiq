import pandas as pd

df = pd.read_csv("data/players_data-2025_2026.csv")

print(df.isnull().sum())

df = df.dropna()

df = df.drop_duplicates()

print(df.head())

df.to_csv("data/clean_players.csv", index=False)