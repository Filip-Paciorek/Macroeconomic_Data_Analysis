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
dff,ahetpi,cpiaucsl,pcepi,unrate = load_data()

def normalize_datetype():

    dff['observation_date'] = pd.to_datetime(dff['observation_date'])
    ahetpi['observation_date'] = pd.to_datetime(ahetpi['observation_date'])
    cpiaucsl['observation_date'] = pd.to_datetime(cpiaucsl['observation_date'])
    pcepi['observation_date'] = pd.to_datetime(pcepi['observation_date'])
    unrate['observation_date'] = pd.to_datetime(unrate['observation_date'])
def normalize_dff_format(dff):
    dff['observation_date'] = pd.to_datetime(dff['observation_date'])
    dff = dff.set_index('observation_date')
    dff.index = pd.to_datetime(dff.index)
    #look for a way to minimize floating point precision error
    dff = dff.resample('ME').mean()
    dff.index = dff.index + pd.offsets.MonthBegin(1)
    dff = dff.reset_index()
    return dff
def normalize_starting_point():
    min = max(dff['observation_date'][0],ahetpi['observation_date'][0],cpiaucsl['observation_date'][0],pcepi['observation_date'][0],unrate['observation_date'][0])
    return min 
def set_starting_date(dff,ahetpi,cpiaucsl,pcepi,unrate):
    min = normalize_starting_point()
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
    return dff,cpiaucsl,ahetpi,pcepi,unrate
dff = normalize_dff_format(dff)
normalize_datetype()
normalize_starting_point()
dff,cpiaucsl,ahetpi,pcepi,unrate = set_starting_date(dff,ahetpi,cpiaucsl,pcepi,unrate)
dff.to_csv('../data/processed/DFF.csv')
cpiaucsl.to_csv('../data/processed/CPIAUCSL.csv')
ahetpi.to_csv('../data/processed/AHETPI.csv')
pcepi.to_csv('../data/processed/PCEPI.csv')
unrate.to_csv('../data/processed/UNRATE.csv')


