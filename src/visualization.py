

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import YearLocator,DateFormatter
df_all = pd.read_csv('../data/processed/dal.csv')
df_all['observation_date'] = pd.to_datetime(df_all['observation_date'])
def format_axes(years):

    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(YearLocator(years))
def all_graphs(df_all):
    plt.figure(figsize=(18,14))
    sns.lineplot(data=df_all,x='observation_date',y='value',hue='variable')
    format_axes(10)
    plt.title('Progress of all variables overtime')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(title='Variable')
    plt.savefig('../plots/all.png')
    print(df_all.head())
    print(df_all['variable'].unique())
def wages_change_over_time(df_all):
    wages_df = df_all[df_all['variable']=='AHETPI']
    plt.figure(figsize=(18,14))
    sns.lineplot(data=wages_df,x='observation_date',y='value')
    format_axes(10)
    plt.title('Changes in wages overtime')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.savefig('../plots/wot1.png')
def wages_vs_inflation(df_all):
    wage_inflation_df = df_all[df_all['variable'].isin(['AHETPI','PCEPI','CPIAUCSL'])]
    plt.figure(figsize=(18,14))
    sns.lineplot(data=wage_inflation_df,x='observation_date',y='value',hue='variable')
    plt.title('Changes in wages overtime compared to inflation')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.savefig('../plots/wvi1.png')
all_graphs(df_all)
wages_change_over_time(df_all)
wages_vs_inflation(df_all)
