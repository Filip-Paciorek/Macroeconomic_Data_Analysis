

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import YearLocator,DateFormatter
df_all = pd.read_csv('../data/processed/dal.csv')
df_all['observation_date'] = pd.to_datetime(df_all['observation_date'])
def format_axes(years):

    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(YearLocator(years))
#might use it
def all_graphs(df_all):
    plt.figure(figsize=(18,14))
    df_wide = df_all.pivot(index='observation_date',columns='variable',values='value')
    corr = df_wide.corr()
    sns.heatmap(corr,annot=True,cmap='coolwarm',center=0)
    plt.title('Heatmap of all variables',fontsize=24)
    plt.savefig('../plots/heatmap.png')
def wages_vs_inflation_lineplot(df_all):
    inflation_df = df_all[df_all['variable'].isin(['PCEPI','CPIAUCSL'])]
    wages_df = df_all[df_all['variable'] == 'AHETPI']
    
    base_year = '2017-01-01'
    base_value = wages_df[wages_df['observation_date'] == base_year]
    wages_df['value'] = (wages_df['value'] / base_value.loc[base_value.index[0],'value']) * 100
    


    fig, ax1 = plt.subplots(figsize=(14,8))
    ax1.grid(True)
    ax1.legend(loc='upper left')
    sns.lineplot(data=inflation_df,x='observation_date',y='value',ax=ax1,hue='variable',palette={'PCEPI':'#E2FF6C','CPIAUCSL':'#44FF51'},lw=2.5)
    #ax2 = ax1.twinx()
    sns.lineplot(data=wages_df,x='observation_date',y='value',ax=ax1,hue='variable',palette={'AHETPI':'#69421F'},lw=2.5)
    #ax2.legend(loc='upper right')
    plt.grid(color='black')
    plt.gca().set_facecolor('#cbf5fc')
    plt.title('Changes in wages overtime compared to inflation',fontsize=24)
    plt.xlabel('Decades',fontsize=20)
    plt.ylabel('Inflation and wages normalized on 2017-01',fontsize=16)
    plt.savefig('../plots/wages_vs_inflation_lineplot.png')
def wages_vs_inflation_barplot(df_all):
    inflation_wages_df = df_all[df_all['variable'].isin(['CPIAUCSL','AHETPI'])]
    inflation_wages_df['decades'] = (inflation_wages_df['observation_date'].dt.year //10) * 10
    inflation_wages_df['decades'] = inflation_wages_df['decades'].map({1960:'1960s',1970:'1970s',1980:'1980s',1990:'1990s',2000:'2000s',2010:'2010s',2020:'2020s'})    
    inflation_df = inflation_wages_df[inflation_wages_df['variable']=='CPIAUCSL']
    aggregated_inflation = inflation_df.groupby('decades')['value'].mean().reset_index()
    wages_df = inflation_wages_df[inflation_wages_df['variable']=='AHETPI']
    base_year = '2017-01-01'
    base_value = wages_df[wages_df['observation_date'] == base_year]
    wages_df['value'] = (wages_df['value'] / base_value.loc[base_value.index[0],'value']) * 100
    aggregated_wages = wages_df.groupby('decades')['value'].mean().reset_index()
    aggregated_inflation_wages = pd.merge(aggregated_wages,aggregated_inflation,on='decades',suffixes=('_wages','_inflation'))
    aggregated_inflation_wages['difference'] = aggregated_inflation_wages['value_wages'] - aggregated_inflation_wages['value_inflation']
    colors = {}
    for iter,row in aggregated_inflation_wages.iterrows():
        decade = row['decades']
        value = row['difference']
        colors[decade] = ('#FF3C00' if value < 0 else '#21F693')
    plt.figure(facecolor='#FFF4A8',figsize=(18,14))
    plt.tight_layout()
    plt.title('Inflation vs wages through the decades (*)',fontsize = 24)
    plt.xlabel('Decades',fontsize = 20)
    plt.ylabel('Difference in % (*)',fontsize=20)
    plt.text(0.01,0.01,'Data normalized for 2017 = 100',transform=plt.gcf().transFigure,fontsize=12,color='gray',va='bottom')
    ax = sns.barplot(data=aggregated_inflation_wages,x='decades',y='difference',hue='decades',palette=colors)
    for container in ax.containers:
        ax.bar_label(container)

    plt.savefig('../plots/wages_vs_inflation_barplot.png')
def phillips_curve(df_all):
    unrate_df = df_all[df_all['variable'] == 'UNRATE']
    inflation_df = df_all[df_all['variable']=='CPIAUCSL']
    base_value = 243.618
    unrate_inflation_df = pd.merge(unrate_df,inflation_df,on='observation_date',suffixes=('_unrate','_inflation'))
    unrate_inflation_df['unnormalized'] = (unrate_inflation_df['value_inflation'] / 100)* base_value
    unrate_inflation_df['YoY_inflation'] = unrate_inflation_df['unnormalized'].pct_change(periods=12)*100
    unrate_inflation_df['decades'] = (unrate_inflation_df['observation_date'].dt.year //10) * 10
    plt.figure(figsize=(18,14))
    plt.tight_layout()
    plt.title('The correlation between unemployment and inflation',fontsize=24)
    plt.xlabel('Unemployment Rate',fontsize=20)
    plt.ylabel('Year on Year Inflation',fontsize=20)
    sns.scatterplot(data=unrate_inflation_df,x='value_unrate',y='YoY_inflation',hue='decades',s=180,marker='X')
    plt.savefig('../plots/phillips_curve.png')
#might use it
def difference_between_inflation_indicators(df_all):
    cpiaucsl_df = df_all[df_all['variable'] == 'CPIAUCSL']
    pcepi_df = df_all[df_all['variable'] == 'PCEPI']
    dates_match = (cpiaucsl_df['observation_date'].reset_index(drop=True)).equals((pcepi_df['observation_date'].reset_index(drop=True)))
    plt.figure(figsize=(18,14))
    sns.lineplot(data=cpiaucsl_df,x='observation_date',y='value',label='CPIAUCSL')
    sns.lineplot(data=pcepi_df,x='observation_date',y='value',label='PCEPI')
    plt.title('Inflation indicators')
    plt.xlabel('Decades')
    plt.ylabel('Indicators')
    plt.legend(title='Indicators')
    plt.savefig('../plots/inflation_indicators_lineplot.png')
    if dates_match:
        #make the histogram recognize decades
        plt.figure(figsize=(18,14))
        inflation_indicators_gap = pd.merge(cpiaucsl_df,pcepi_df,on='observation_date',suffixes=('_cpiaucsl','_pcepi'))
        inflation_indicators_gap['difference'] = inflation_indicators_gap['value_cpiaucsl'] - inflation_indicators_gap['value_pcepi']
        inflation_indicators_gap['decades'] = (inflation_indicators_gap['observation_date'].dt.year //10 ) * 10
        sns.histplot(inflation_indicators_gap['difference'],bins=30,kde=True)
        plt.savefig('../plots/inflation_indicators_hist.png')
    else:
        dates1 = pcepi_df['observation_date']
        dates2 = cpiaucsl_df['observation_date']
        missing_pcepi = dates1[~dates1.isin(dates2)]
        missing_cpiaucsl = dates2[~dates2.isin(dates1)]
        print('Dates don\'t match here:')
        print(missing_cpiaucsl.values)
        print(missing_pcepi.values)
    format_axes(10)
def unemployment_rate_avg_through_decades(df_all):
    unrate_df = df_all[df_all['variable'] == 'UNRATE']
    unrate_df['month'] = (unrate_df['observation_date'].dt.year // 10) * 10
    unrate_df['decades'] = unrate_df['month'].map({1960:'1960s',1970:'1970s',1980:'1980s',1990:'1990s',2000:'2000s',2010:'2010s',2020:'2020s'})
    aggregated = unrate_df.groupby('decades')['value'].mean().reset_index()
    max_decade = aggregated.loc[aggregated['value'].idxmax(),'decades']
    min_decade = aggregated.loc[aggregated['value'].idxmin(),'decades']
    colors = {decade:('#fa4a4a' if decade == max_decade else '#00cc00' if decade==min_decade else '#a18989') for decade in aggregated['decades']}
    custom_params = {'axes.spines.right': False,'axes.spines.top':False}
    plt.figure(figsize=(18,14))
    plt.tight_layout()
    plt.gca().set_facecolor('#DBDB6B')
    sns.set_theme(style='ticks',rc=custom_params)
    plt.title('Unemployment rate through decades',fontsize=24)
    plt.ylabel('% of unemployment',fontsize=20)
    plt.xlabel('decades',fontsize=20)
    ax = sns.barplot(data=aggregated,x='decades',y='value',hue='decades',palette=colors)
    for container in ax.containers:
        ax.bar_label(container)
    plt.savefig('../plots/unemployment_seasons.png')

unemployment_rate_avg_through_decades(df_all)
difference_between_inflation_indicators(df_all)
all_graphs(df_all)
phillips_curve(df_all)
wages_vs_inflation_lineplot(df_all)
wages_vs_inflation_barplot(df_all)
