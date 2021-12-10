# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:10:10 2021''

@author: Konsulenten
"""
#%%

#import libraries
import pandas as pd
import pycountry 

#Load data
df = pd.read_excel('crashes.xlsx')

#Drop columns of no interest
df = df.drop(columns="Registration")
df = df.drop(columns="Cn_ln")



#%%
# Mutate data in df to eliminate undesireable notations




#%%
# Create country list, mutate countries spelled undesireable
country_list = []
iso_list = []
country_df = pd.DataFrame(columns=['country','ISO'])
for i in pycountry.countries:
    country_list.append(i.name)
    iso_list.append(i.alpha_2)

#Alterations of incorrect country names
country_list[13] = 'Antigua'
country_list[20] = 'Netherlands Antilles'
country_list[26] = 'Bosnia'
country_list[31] = 'Bolivia'
country_list[34] = 'Brunei'
country_list[40] = 'Cocos Islands'
country_list[44] = 'Ivory Coast'
country_list[46] = 'Democratic Republic Congo'
country_list[54] = 'Curacao'
country_list[58] = 'Czechoslovakia'
country_list[77] = 'Micronesia'
country_list[107] = 'Iran'
country_list[122] = 'South Korea'
country_list[144] = 'Macedonia'
country_list[181] = 'North Korea'
country_list[184] = 'Palestine'
country_list[189] = 'Russia'
country_list[214] = 'Syria'
country_list[222] = 'Timor'
country_list[224] = 'Trinidad'
country_list[228] = 'Taiwan'
country_list[229] = 'Tanzania'
country_list[238] = 'Venezuela'
country_list[241] = 'Vietnam'

# Create Country and ISO dataframe
country_df['country'] = country_list
country_df['ISO'] = iso_list

# Tilføjer amrikanske stater til country og ISO list + District of Columbia
state_names = pd.DataFrame([["Alaska", 'US'], ["Alabama", 'US'], ["Arkansas", 'US'], ["Arizona", 'US'], ["California", 'US'], ["Colorado", 'US'], ["Connecticut", 'US'], ["D.C.", 'US'], ["Delaware", 'US'], ["Florida", 'US'], ["Georgia", 'US'], ["Hawaii", 'US'], ["Iowa", 'US'], ["Idaho", 'US'], ["Illinois", 'US'], ["Indiana", 'US'], ["Kansas", 'US'], ["Kentucky", 'US'], ["Louisiana", 'US'], ["Massachusetts", 'US'], ["Maryland", 'US'], ["Maine", 'US'], ["Michigan", 'US'], ["Minnesota", 'US'], ["Missouri", 'US'], ["Mississippi", 'US'], ["Montana", 'US'], ["North Carolina", 'US'], ["North Dakota", 'US'], ["Nebraska", 'US'], ["New Hampshire", 'US'], ["New Jersey", 'US'], ["New Mexico", 'US'], ["Nevada", 'US'], ["New York", 'US'], ["Ohio", 'US'], ["Oklahoma", 'US'], ["Oregon", 'US'], ["Pennsylvania", 'US'], ["Rhode Island", 'US'], ["South Carolina", 'US'], ["South Dakota", 'US'], ["Tennessee", 'US'], ["Texas", 'US'], ["Utah", 'US'], ["Virginia", 'US'], ["Vermont", 'US'], ["Washington", 'US'], ["Wisconsin", 'US'], ["West Virginia", 'US'], ["Wyoming", 'US']], columns=['country', 'ISO'])

country_df = country_df.append(state_names)

# Sort country-ISO dataframe descending
country_df = country_df.sort_values(by='country',ascending=False)



#%%
# Dataframe for all cities with population above 15.000
city_list = pd.read_csv('cities_of_the_world.csv')



#%%
# Function: 
#    Iterate and get crash country name and ISO code. Append to df. 
###

def country_ISO_miner(data, country_iso_df, col_target):
    data_copy = data.copy()
    ISO_list = []
    country_list = []
    
    
    for index_df, row_df in data_copy.iterrows():
        nan_applier = True
        
        for index, row in country_iso_df.iterrows():
            if row['country'] in str(row_df[col_target]).replace(',', ''):
                ISO_list.append(row['ISO'])
                country_list.append(row['country'])
                print('NAME activated INDEX:',index_df)
                nan_applier = False
                break
            
            else:
                word_list = []
                sentence = str(row_df[col_target]).replace(',', '')
                word_list.append(sentence.split(' '))
                
                if row['ISO'] in word_list:                
                    ISO_list.append(row['ISO'])
                    country_list.append(row['country'])
                    print('ISO activated INDEX:',index_df)
                    nan_applier = False
                    break
                
        if nan_applier == True:        
            ISO_list.append(None)
            country_list.append(None)
            
    
    country_col_name = col_target + '_country'
    ISO_col_name = col_target + '_ISO'
    
    data_copy[country_col_name] = country_list
    data_copy[ISO_col_name] = ISO_list
    
    
    return data_copy

def passenger_splitter(df):
    df[['total_passengers_num','passengers_alive','crew_alive']] = df['onboard_alive'].str.split('Â', expand=True)
    df['passengers_alive'] = df['passengers_alive'].str.split(':').str[-1]
    df['crew_alive'] = df['crew_alive'].str.split(':').str[-1]
    df['crew_alive'] = df['crew_alive'].str.split(')').str[0]
    df[['total_passengers_dead','passengers_dead','crew_dead']] = df['Onboard_fatalities_num'].str.split('Â', expand=True)
    df['passengers_dead'] = df['passengers_dead'].str.split(':').str[-1]
    df['crew_dead'] = df['crew_dead'].str.split(':').str[-1]
    df['crew_dead'] = df['crew_dead'].str.split(')').str[0]
    return df

#%%
# Split crash_site in ISO and country, append to df and drop na values
df['Crash_location'].replace('USSR','Russia')
df = country_ISO_miner(df, country_df, 'Crash_location')
df.dropna(inplace=True)

#%%
df = passenger_splitter(df)


#%%

df[['total_passengers_num','passengers_alive','crew_alive']] = df['passengers_alive'].str.split('Â', expand=True)
df['passengers_alive'] = df['passengers_alive'].str.split(':').str[-1]
df['crew_alive'] = df['crew_alive'].str.split(':').str[-1]
df['crew_alive'] = df['crew_alive'].str.split(')').str[0]
#%%













#%%
# The old loop, MAthias x Jakob
###
valid_index = []
crash_ISO = []
crash_country = []
i = 0

for index_df, row_df in df.iterrows():
    #print(i)
    for index, row in country_df.iterrows():
        if row['country'] in str(row_df['Crash_location']).replace(',', ''):
            crash_ISO.append(row['ISO'])
            crash_country.append(row['country'])
            valid_index.append(i)
            print('NAME activated INDEX:',index_df)
            break
        elif row['ISO'] in str(row_df['Crash_location']).replace(',', ''):
            crash_ISO.append(row['ISO'])
            crash_country.append(row['country'])
            valid_index.append(i)
            print('ISO activated INDEX:',index_df)
            break
    i +=1
print(valid_index)


#%%

valid_index = []
crash_ISO = []
crash_country = []
i = 0

dfc = df.copy(deep=True)


for index_df, row_df in dfc.iterrows():
    nan_applier = True
    #print(i)
    for index, row in country_df.iterrows():
        if row['country'] in str(row_df['Crash_location']).replace(',', ''):
            crash_ISO.append(row['ISO'])
            crash_country.append(row['country'])
            valid_index.append(i)
            print('NAME activated INDEX:',index_df)
            nan_applier = False
            break
        else:
            word_list = []
            #e=0
            sentence = str(row_df['Crash_location']).replace(',', '')
            word_list.append(sentence.split(' '))
            if row['ISO'] in word_list:                
                crash_ISO.append(row['ISO'])
                crash_country.append(row['country'])
                valid_index.append(i)
                print('ISO activated INDEX:',index_df)
                nan_applier = False
                break
    if nan_applier == True:        
        crash_ISO.append(None)
        crash_country.append(None)
        valid_index.append(None)
    
    i +=1
print(valid_index)

dfc['Crash_country'] = crash_country
dfc['Crash_ ISO'] = crash_ISO


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

