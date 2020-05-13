import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

z = 1.96 # define the z-value, 1.96 for 95% confidence interval

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

# function to generate a bar's colour
# based on the selected y value and the mean and confidence interval of the bar
def colour(y_value, mean, interval):
    colour = 'blue'
    return colour


df = get_stats(get_data(12345), 1.96)

# creat figure and plot the data
fig, ax = plt.subplots()
ax.bar(df.index, df['mean'], yerr = df['error'])

plt.show()