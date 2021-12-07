# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:10:10 2021''

@author: Konsulenten
"""
#%%
#import libraries
from numpy.lib.function_base import append
import pandas as pd
import pycountry 


#Load data
df = pd.read_excel('crashes.xlsx')

#Drop columns of no interest
df = df.drop(columns="Registration")
df = df.drop(columns="Cn_ln")

#Split colum 'route' and create two new 'from', 'to'
#df[['From', 'To']] = df['Route'].str.split(' - ', 1, expand=True)
#split month and data 'Date' into 'Month' and 'Date'--last replacing the origin
#df[['Month', 'Date']] = df['Date'].str.split(' ', 1, expand=True)
# %%
#
df.dropna(inplace=True)

#%%
country_list = []
iso_list = []
country_df = pd.DataFrame(columns=['country','ISO'])
for i in pycountry.countries:
    country_list.append(i.name)
    iso_list.append(i.alpha_2)

country_df['country'] = country_list
country_df['ISO'] = iso_list



#%%
valid_index = []
crash_ISO = []
crash_country = []
i = 0

for index_df, row_df in df.iterrows():
    #print(i)
    for index, row in country_df.iterrows():
        if row['country'] in str(row_df['Crash_location']):
            crash_ISO.append(row['ISO'])
            crash_country.append(row['country'])
            valid_index.append(i)
            print('NAME activated INDEX:',index_df)
            break
        elif row['ISO'] in str(row_df['Crash_location']):
            crash_ISO.append(row['ISO'])
            crash_country.append(row['country'])
            valid_index.append(i)
            print('ISO activated INDEX:',index_df)
            break
    i +=1
print(valid_index)


#%%





#%%
#
df[['Cr_city', 'Cr_country']] = df['Crash_location'].str.split(', ', 1, expand=True)
df[['Cr_region', 'Cr_country']] = df['Cr_country'].str.split(', ', 1, expand=True)
df[['total_passengers_num','passengers_alive','crew_alive']] = df['Passenegrs_num'].str.split('Â', expand=True)
df['passengers_alive'] = df['passengers_alive'].str.split(':').str[-1]
df['crew_alive'] = df['crew_alive'].str.split(':').str[-1]
df['crew_alive'] = df['crew_alive'].str.split(')').str[0]

df = df.drop(columns= ['Crash_location','Route','Passenegrs_num'])
#%%
countries = []
countries.append(pycountry.countries)

print(countries)

#%%
#Print statement for all collumn uniques and count of number of collumn variables
for col in df:
    print('For column',col,'number of uniques are:')
    print(len(df[col].value_counts(dropna=False)))
    print('-The uniques are:')
    print(df[col].unique())
    print('...')


# %%
#df.to_excel('Wrangled_data.xlsx')

