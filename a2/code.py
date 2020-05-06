import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplleaflet
import pandas as pd
import numpy as np
import datetime as dt

def data_preprocessing():
    # function to read and clean csv data
    # returns two DataFrame objects
    # df      = min/max temps observed for each day of the year for 2005-2014 (365 data points)
    # df_2015 = min/max temps observed for each day of the year for 2015 (365 data points)
    
    # first read the csv file to a DataFrame object
    df = pd.read_csv('C2A2_data.csv')
    
    # sort by date (dates are stored as a string)
    df = df.sort_values(by='Date').drop('ID', 1)
    
    # get overall min and max for each date and store in df
    df_min = df[df['Element'] == 'TMIN'].groupby('Date', as_index=False)['Data_Value'].min().rename(columns={'Data_Value':'TMIN'})
    df_max = df[df['Element'] == 'TMAX'].groupby('Date', as_index=False)['Data_Value'].max().rename(columns={'Data_Value':'TMAX'})
    df = df_min.join(df_max.set_index('Date'), on='Date')
    
    # remove leap year dates (XXXX-02-29)
    df = df[~df['Date'].str.contains('-02-29')]
    
    # convert from 'tenths of degree C' to 'degree C float'
    df['TMIN'] = df['TMIN'] / 10.0
    df['TMAX'] = df['TMAX'] / 10.0
    
    # split 2015 year from data
    df_2015 = df[df['Date'].str.contains('2015-')] # df for only year 2015
    df = df[~df['Date'].str.contains('2015-')]     # df for years 2005-2014
    
    # remove year part of the Date
    df['Date'] = df['Date'].map(lambda x: x[5:])
    df_2015['Date'] = df_2015['Date'].map(lambda x: x[5:])
    
    # get min and max for each day of the year
    df_min = df.groupby('Date', as_index=False)['TMIN'].min()
    df_max = df.groupby('Date', as_index=False)['TMAX'].max()
    df = df_min.join(df_max.set_index('Date'), on='Date')
    
    # convert MM-DD to mpl datetime
    df['Date'] = pd.to_datetime( df['Date'], format='%m-%d' )
    df_2015['Date'] = pd.to_datetime( df_2015['Date'], format='%m-%d' )
    
    return df.reset_index(drop=True), df_2015.reset_index(drop=True)

def get_records_broken(df_A, df_B):
    # function to get points (dates) in df_A that break max/min records in df_B
    # returns a df where records are broken (NaN where records are not broken)
    
    df = pd.DataFrame(columns=['Date', 'TMIN', 'TMAX'])
    
    for index, row in df_A.iterrows():
        t_date = row['Date']
        t_min = np.nan
        t_max = np.nan
        if row['TMIN'] < df_B.iloc[index]['TMIN']:
            t_min = row['TMIN']
        if row['TMAX'] > df_B.iloc[index]['TMAX']:
            t_max = row['TMAX']
        
        df = df.append( {'Date': t_date, 'TMIN': t_min, 'TMAX': t_max}, ignore_index=True )

    return df

# set plot ink color
colour = "#5c5c5c"

# set default font
plt.rcParams.update({'font.size': 13})

# get the data to plot
df, df_2015 = data_preprocessing()
df_broken = get_records_broken(df_2015, df)

# create figure object
fig = plt.figure(figsize=(10.0,7.0))
ax = fig.add_subplot(1, 1, 1)
fig.patch.set_facecolor('white')

# set the x axis labelling
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xlim([dt.date(1900, 1, 1), dt.date(1900, 12, 31)])

# plot the two lines
ax.plot(df['Date'], df['TMAX'], color='darkorange', linewidth=2.0, label="Record highs observed on each day over 2005-2014")
ax.plot(df['Date'], df['TMIN'], color='lightskyblue', linewidth=2.0, label="Record lows observed on each day over 2005-2014")

# fill the area between the two line plots
ax.fill_between(df.Date.values, df.TMIN.values, df.TMAX.values, facecolor='slategrey', alpha=0.15)

# plot the 2015 record breakinf points as a scatter plot
ax.scatter(df.Date.values, df_broken.TMIN.values, color='maroon', zorder=10, label="Records broken over 2015")
ax.scatter(df.Date.values, df_broken.TMAX.values, color='maroon', zorder=10)

# add title
ax.set_title('Record Temperatures (°C) near Ann Arbor, Michigan (2005-2015)'
          , color=colour
          , wrap=True
          , fontsize='large'
          )

# shift xtick labels to the right and hide xtick lines
x_ticks = []
for tick in ax.get_xticks():
    tick += 15.0
    x_ticks.append(tick)
ax.set_xticks(x_ticks)
ax.tick_params(axis='both', colors=colour)
ax.tick_params(axis='x', colors='w', labelcolor=colour)

# move x labels to the top
ax.xaxis.tick_top()

# adjust title spacing
ax.title.set_position([.5, 1.07])

# change ytick spacing 
ax.yaxis.set_ticks(np.arange(-20, 50, 20))

# add legend
leg = ax.legend(edgecolor='white')
plt.setp(leg.get_texts(), color=colour)

# remove frame around plot
for spine in ax.spines.values():
    spine.set_visible(False)

plt.show()
