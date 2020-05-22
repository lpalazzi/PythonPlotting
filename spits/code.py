import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import markers

# draft data from https://www.hockey-reference.com/play-index/draft_finder.cgi (picked in first 300)
# season by season data from https://www.hockeydb.com/stte/windsor-spitfires-10926.html

# read datasets from csv files
df_draft = pd.read_csv("draft_data.csv")
df_season = pd.read_csv("season_data.csv")

# trim down and process data
df_season = df_season[['Season', 'W', 'L', 'T', 'Pts', 'Pct', 'Atten.', 'Result']].rename(columns={'Season': 'Year', 'Atten.': 'Average Attendance', 'Pct': 'Win Percentage'}).set_index('Year')
df_draft = df_draft[['Year']].groupby(by=df_draft.Year, axis=0, as_index=True).count().rename(columns={'Year': 'Drafted'}) # NOTE: years with no drafted players are not included in this df

# join datasets into one DataFrame
df = df_season.join(df_draft, how='left')

# fix null values in the drafted players column
df['Drafted'].fillna(0, inplace = True)
df['Drafted'] = df['Drafted'].astype('int64')

# set plot ink colour
inkColour = "#5c5c5c"

# create the figure object
fig, ax1 = plt.subplots(sharex=True, figsize=(14.0,3.0), facecolor='white')

# plot the win percentages
colour = 'darkblue'
ax1.set_xlabel('Season (Year)', color=inkColour)
ax1.set_ylabel('Win Percentage', color=colour)
ax1.set(ylim=(0.25,1.0))
ax1.xaxis.set_ticks(np.arange(min(df.index), max(df.index), 2))
ax1.plot(df['Win Percentage'], color=colour)
ax1.tick_params(axis='y', labelcolor=colour)
ax1.tick_params(axis='x', colors='w', labelcolor=inkColour)

# instantiate a second axis that inherits the first axis
ax2 = ax1.twinx()

# plot the drafted players
colour = 'darkred'
ax2.set_ylabel('Players Drafted (Top 300 Picks)', color=colour)
ax2.plot(df['Drafted'], color=colour)
ax2.tick_params(axis='y', labelcolor=colour)
ax2.yaxis.set_ticks(np.arange(0, 6, 1))

# plot the points for when the team won a championship
x = []
y = []
for index, row in df.iterrows():
    result = str(row['Result'])
    if 'Won Championship' in result:
        x.append(row.name)
        y.append(row['Win Percentage'])
ax1.scatter(x, y, color='gold', marker='*', linewidths=1.0, edgecolors='black', zorder=10, s=150, label = 'Won Championship')

# add legend
leg = ax1.legend(edgecolor='white', scatterpoints=1)
plt.setp(leg.get_texts(), color=inkColour)

# set the title for the plot
ax1.set_title('Windsor Spitfires: Season Win Percentage vs. Number of Players Drafted to NHL'
          , color=inkColour
          , wrap=True
          , fontsize='large'
          )

# remove frame around plot
for spine in ax1.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

#fig.tight_layout()

plt.show()