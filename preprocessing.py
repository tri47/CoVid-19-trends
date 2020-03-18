import numpy as numpy
import pandas as pd

dataSets = ['Confirmed', 'Recovered', 'Deaths']

datas = {}

for data_name in dataSets:
    df = pd.read_csv(data_name + '.csv')
    max_ix = df.shape[0]
    df.loc[max_ix,:]= df[df['Country/Region'] != 'China'].sum(axis=0)
    df.loc[max_ix,'Country/Region'] = 'Rest of the World'
    df.loc[max_ix+1,:]= df[df['Country/Region'] != 'Rest of the World'].sum(axis=0)
    df.loc[max_ix+1,'Country/Region'] = 'Worldwide'
    Cases = pd.melt(df, id_vars= ['Province/State','Country/Region','Lat','Long'],var_name='dateString',value_name=data_name)
    Cases[['month','day','year']] = Cases.dateString.str.split('/',expand=True)
    Cases['date'] = Cases.day + '/' + Cases.month + '/' + Cases.year
    Cases.drop(['month','day','year','dateString'],axis=1,inplace=True)
    datas[data_name] = Cases


df_cd = datas['Confirmed'].merge(datas['Deaths'].loc[:,['Country/Region','Province/State','date','Deaths']], on=['Country/Region','Province/State', 'date'], how='left')

df = df_cd.merge(datas['Recovered'].loc[:,['Country/Region','Province/State','date','Recovered']], on=['Country/Region', 'Province/State','date'], how='left')

print(df.describe())

df.to_csv('CovData.csv',index=False)
