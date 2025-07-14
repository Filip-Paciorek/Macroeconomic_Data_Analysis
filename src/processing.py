'''
Functions' explanation:
 * load_data() - loads the data from the csv to df
 * normalize_datetype() - deals with inconsistencies of value type (some were datetime, some were string)
 * normalize_dff_format() - dff was the only outlier when it comes to measurment of the data (daily vs monthly)
 * normalize_starting_point() - finds the earliest date that all datasets contain 
 * set_starting_date() - sets the date to the earlier found one 
 * turn_into_long_format() - transforms the df into a format better suited for merging with otherdfs
 * merge() - merges all the dfs together
 * synchronise_inflation_indicators() - fixes the normalization of CPIAUCSL and PCEPI
    
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    dff = pd.read_csv('../data/raw/DFF.csv')
    ahetpi = pd.read_csv('../data/raw/AHETPI.csv')
    cpiaucsl = pd.read_csv('../data/raw/CPIAUCSL.csv')
    pcepi = pd.read_csv('../data/raw/PCEPI.csv')
    unrate = pd.read_csv('../data/raw/UNRATE.csv')
    return dff,ahetpi,cpiaucsl,pcepi,unrate

def normalize_datetype(dff,ahetpi,cpiaucsl,pcepi,unrate):
    dff['observation_date'] = pd.to_datetime(dff['observation_date'])
    ahetpi['observation_date'] = pd.to_datetime(ahetpi['observation_date'])
    cpiaucsl['observation_date'] = pd.to_datetime(cpiaucsl['observation_date'])
    pcepi['observation_date'] = pd.to_datetime(pcepi['observation_date'])
    unrate['observation_date'] = pd.to_datetime(unrate['observation_date'])

def normalize_dff_format(dff):
    dff['observation_date'] = pd.to_datetime(dff['observation_date'])
    dff = dff.set_index('observation_date')
    dff.index = pd.to_datetime(dff.index)
    dff = dff.resample('ME').mean()
    dff.index = dff.index + pd.offsets.MonthBegin(1)
    dff = dff.reset_index()
    return dff

def normalize_starting_point(dff,ahetpi,cpiaucsl,pcepi,unrate):
    min = max(dff['observation_date'][0],ahetpi['observation_date'][0],cpiaucsl['observation_date'][0],pcepi['observation_date'][0],unrate['observation_date'][0])
    return min 

def set_starting_date(dff,ahetpi,cpiaucsl,pcepi,unrate):
    min = normalize_starting_point(dff,ahetpi,cpiaucsl,pcepi,unrate)
    dff_index = dff[dff['observation_date']==min].index[0]
    cpiaucsl_index = cpiaucsl[cpiaucsl['observation_date']==min].index[0]
    ahetpi_index = ahetpi[ahetpi['observation_date']==min].index[0]
    pcepi_index = pcepi[pcepi['observation_date']==min].index[0]
    unrate_index = unrate[unrate['observation_date']==min].index[0]
    dff = dff.iloc[dff_index:].reset_index(drop=True)
    cpiaucsl = cpiaucsl.iloc[cpiaucsl_index:].reset_index(drop=True)
    ahetpi = ahetpi.iloc[ahetpi_index:].reset_index(drop=True)
    pcepi = pcepi.iloc[pcepi_index:].reset_index(drop=True)
    unrate = unrate.iloc[unrate_index:].reset_index(drop=True)
    return dff,ahetpi,cpiaucsl,pcepi,unrate
def synchronise_inflation_indicators(cpiaucsl):
    base_year = '2017-01-01'
    series_cpiaucsl = cpiaucsl.copy()
    base_value = series_cpiaucsl.loc[series_cpiaucsl['observation_date']==base_year,'CPIAUCSL']
    cpiaucsl['CPIAUCSL'] = (series_cpiaucsl['CPIAUCSL'] / base_value.iloc[0])*100
    print(cpiaucsl.head())
    return cpiaucsl
def turn_into_long_format(dff,ahetpi,cpiaucsl,pcepi,unrate):
    dff_long = dff.rename(columns={'DFF':'value'})
    ahetpi_long = ahetpi.rename(columns={'AHETPI':'value'})
    cpiaucsl_long = cpiaucsl.rename(columns={'CPIAUCSL':'value'})
    pcepi_long = pcepi.rename(columns={'PCEPI':'value'})
    unrate_long = unrate.rename(columns={'UNRATE':'value'})

    dff_long['variable'] = 'DFF'
    ahetpi_long['variable'] = 'AHETPI'
    cpiaucsl_long['variable'] = 'CPIAUCSL'
    pcepi_long['variable'] = 'PCEPI'
    unrate_long['variable'] = 'UNRATE'
    return dff_long,ahetpi_long,cpiaucsl_long,pcepi_long,unrate_long
def merge(dff_long,ahetpi_long,cpiacusl_long,pcepi_long,unrate_long):
    df_all_long = pd.concat([dff_long,ahetpi_long,cpiacusl_long,pcepi_long,unrate_long],ignore_index=True)
    return df_all_long
dff,ahetpi,cpiaucsl,pcepi,unrate = load_data()
dff = normalize_dff_format(dff)
normalize_datetype(dff,ahetpi,cpiaucsl,pcepi,unrate)
dff,ahetpi,cpiaucsl,pcepi,unrate = set_starting_date(dff,ahetpi,cpiaucsl,pcepi,unrate)
cpiaucsl = synchronise_inflation_indicators(cpiaucsl)
dff_long,ahetpi_long,cpiaucsl_long,pcepi_long,unrate_long = turn_into_long_format(dff,ahetpi,cpiaucsl,pcepi,unrate)
df_all_long = merge(dff_long,ahetpi_long,cpiaucsl_long,pcepi_long,unrate_long)
df_all_long.to_csv('../data/processed/dal.csv')
dff.to_csv('../data/processed/DFF.csv')
cpiaucsl.to_csv('../data/processed/CPIAUCSL.csv')
ahetpi.to_csv('../data/processed/AHETPI.csv')
pcepi.to_csv('../data/processed/PCEPI.csv')
unrate.to_csv('../data/processed/UNRATE.csv')


