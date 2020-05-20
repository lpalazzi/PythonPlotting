import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data():
    # draft data from https://www.hockey-reference.com/play-index/draft_finder.cgi (picked in first 300)
    # season by season data from https://www.hockeydb.com/stte/windsor-spitfires-10926.html

    # read datasets from csv files
    df_draft = pd.read_csv("draft_data.csv")
    df_season = pd.read_csv("season_data.csv")

    # trim down and process data
    df_season = df_season[['Season', 'W', 'L', 'T', 'Pts', 'Pct', 'Atten.', 'Result']].rename(columns={'Season': 'Year'}).set_index('Year')
    df_draft = df_draft[['Year']].groupby(by=df_draft.Year, axis=0, as_index=True).count().rename(columns={'Year': 'Drafted Players'}) # NOTE: years with no drafted players are not included in this df

    # join datasets into one DataFrame
    df = df_season.join(df_draft, how='left')
    df['Drafted Players'].fillna(0, inplace = True)
    df['Drafted Players'] = df['Drafted Players'].astype('int64')
    return df

print (get_data())