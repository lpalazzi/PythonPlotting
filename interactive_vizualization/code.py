import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
import math

z = 1.96 # define the z-value, 1.96 for 95% confidence interval
y_value = 0.0 # default y-value to set the colours before the first user-click

# set cmap
#cmap = cm.coolwarm
cmap = cm.get_cmap("coolwarm")

def get_data(rand_seed):
    # generate bar chart data for the plot
    np.random.seed(rand_seed)
    df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                    np.random.normal(43000,100000,3650), 
                    np.random.normal(43500,140000,3650), 
                    np.random.normal(48000,70000,3650)], 
                    index=[1992,1993,1994,1995])
    return df

def get_error(z, std, n):
    # function to get error bar intervals for a given z-value, standard deviation, and sample size
    return ( z * (std / math.sqrt( n )) )

def get_stats(df, z):
    # get the means and confidence intervals for the input DataFrame
    # df = input dataframe
    # z = z-value for the confidence interval (1.96 for 95%)
    
    # calculate required summary statistics
    means = df.mean(axis=1)
    stds = df.std(axis=1)
    size = df.count(axis=1)

    # combine summary stats into one df
    stats = pd.concat([means, stds, size], axis=1).rename(columns={0:'mean', 1:'std', 2:'size'})

    # calculate margin of error (error bars) for each year
    stats['error'] = np.nan
    for index, row in stats.iterrows():
        stats.at[index, 'error'] = get_error(z=z, std=row['std'], n=row['size'])

    return stats

def colour(y_value, mean, error):
    # function to generate a bar's colour
    # based on the selected y value and the mean and confidence interval of the bar
    lower_bound = mean - error
    upper_bound = mean + error
    norm = colors.Normalize(vmin=lower_bound, vmax=upper_bound)

    if y_value < lower_bound:
        return cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(lower_bound)
    elif y_value > upper_bound:
        return cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(upper_bound)
    else:
        return cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(y_value)

def onclick(event):
    # store y location of the user-click
    y_value = event.ydata
    if y_value == None:
        return # do nothing if user clicks outside the plot
    
    # determine the new colours based on the updated y-value
    for index, row in df.iterrows():
        df.at[index, 'colour'] = colour(y_value = y_value, mean = row['mean'], error = row['error'])

    # re-plot the data with updated colours
    plt.cla()
    plt.bar(df.index, df['mean'], yerr = df['error'], color = df['colour'])
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plt.axhline(y=y_value)
    plt.gca().set_xlabel('Year')
    plt.annotate('y = ' + str(int(y_value)), [df.index[0], 50000])
    plt.show()

    return

# preprocess the data, store stats for plotting in df
df = get_stats(get_data(12345), 1.96)

# set the default bar colours 
df['colour'] = ''
for index, row in df.iterrows():
    df.at[index, 'colour'] = colour(y_value = y_value, mean = row['mean'], error = row['error'])

# creat figure and plot the data
plt.figure()
plt.bar(df.index, df['mean'], yerr = df['error'], color = df['colour'])
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.gca().set_xlabel('Year')
plt.gcf().canvas.mpl_connect('button_press_event', onclick)
plt.show()