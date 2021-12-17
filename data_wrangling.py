# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:10:10 2021''

@author: Konsulenten
"""
#%%

#import libraries
import numpy as np
import pandas as pd
import pycountry 

#Load data
df = pd.read_excel('crashes.xlsx')
#Drop columns of no interest
df = df.drop(columns="Registration")
df = df.drop(columns="Cn_ln")


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
state_names = pd.DataFrame([["Alaska", 'US'], ["Alabama", 'US'], 
                            ["Arkansas", 'US'], ["Arizona", 'US'], 
                            ["California", 'US'], ["Colorado", 'US'], 
                            ["Connecticut", 'US'], ["D.C.", 'US'], 
                            ["Delaware", 'US'], ["Florida", 'US'], 
                            ["Georgia", 'US'], ["Hawaii", 'US'], 
                            ["Iowa", 'US'], ["Idaho", 'US'], 
                            ["Illinois", 'US'], ["Indiana", 'US'], 
                            ["Kansas", 'US'], ["Kentucky", 'US'], 
                            ["Louisiana", 'US'], ["Massachusetts", 'US'], 
                            ["Maryland", 'US'], ["Maine", 'US'], 
                            ["Michigan", 'US'], ["Minnesota", 'US'], 
                            ["Missouri", 'US'], ["Mississippi", 'US'], 
                            ["Montana", 'US'], ["North Carolina", 'US'], 
                            ["North Dakota", 'US'], ["Nebraska", 'US'], 
                            ["New Hampshire", 'US'], ["New Jersey", 'US'], 
                            ["New Mexico", 'US'], ["Nevada", 'US'], 
                            ["New York", 'US'], ["Ohio", 'US'], 
                            ["Oklahoma", 'US'], ["Oregon", 'US'], 
                            ["Pennsylvania", 'US'], ["Rhode Island", 'US'], 
                            ["South Carolina", 'US'], ["South Dakota", 'US'], 
                            ["Tennessee", 'US'], ["Texas", 'US'], 
                            ["Utah", 'US'], ["Virginia", 'US'], 
                            ["Vermont", 'US'], ["Washington", 'US'], 
                            ["Wisconsin", 'US'], ["West Virginia", 'US'], 
                            ["Wyoming", 'US']], columns=['country', 'ISO'])

country_df = country_df.append(state_names)

# Sort country-ISO dataframe descending
country_df = country_df.sort_values(by='country',ascending=False)



#%%
# Dataframe for all cities with population above 5.000
cities_list = pd.read_csv('cities5000.txt', sep="\t", header=None)
cities_list = cities_list[[1,4,5,8]]
cities_list.columns=['city_name','longitude','latitude','ISO']


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

def city_miner(data, cities_list, col_target):
    data_copy = data.copy()
    city_list = []
    long_list = []
    lat_list = []
    
    for index_df, row_df in data_copy.iterrows():
        nan_applier = True
        for index, row in cities_list.iterrows():
            if row['city_name'] in str(row_df[col_target]).replace(',', ''):
                print(row['city_name'])
                if row['ISO'] == row_df['Crash_location_ISO']:
                    print(row['ISO'])
                    city_list.append(row['city_name'])
                    long_list.append(row['longitude'])
                    lat_list.append(row['latitude'])
                    nan_applier = False
        
                    break
        print('next')
        if nan_applier == True:        
            city_list.append(None)
            long_list.append(None)
            lat_list.append(None)
            
    
    city_col_name = col_target + '_city'
    long_col_name = col_target + '_city_longitude'
    lati_col_name = col_target + '_city_latitude'

    data_copy[city_col_name] = city_list
    data_copy[long_col_name] = long_list
    data_copy[lati_col_name] = lat_list
    
    
    return data_copy

#Splits the columns of [onboard_alive,onboard_fatalities_num] into three new columns for both of them, total, passengers and crew
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

#%%
# Get crash city and coordinates for crash sites

df = city_miner(df, cities_list, 'Crash_location')
df.to_csv('trimmed_crashes_city5k.csv')

#%%
df = pd.read_csv('crashes_to_visualize.csv')


#%%
# Call the function for splitting passengers alive dataframes and dead into seperate columns
df = passenger_splitter(df)
df.drop(['onboard_alive','Onboard_fatalities_num'])
df = df.drop(columns=['onboard_alive','Onboard_fatalities_num'])
df = df.drop(df.columns[0], axis=1)


#%%
# Turn all dataset '?' into None, and add total fatalities and survivor counts


df_org = df

df = df.rename(columns={"total_passengers_num": "Total onboard", 
                        "passengers_alive": "Passengers onboard", 
                        "crew_alive": "Crew onboard", 
                        "Total dead": "Onboard deaths", 
                        "passengers_dead": "Passengers dead", 
                        "crew_dead": "Crew dead"})

#%%
df["all deaths"] = df["Onboard deaths"] + df["Ground_fatalities_num"]
#%%

#%%

df['Summary'] = df['Summary'].replace('?', 'Summary unavailable.')
df = df.replace('?', None)
df = df.replace('? ', None)
#%%

df ["Total onboard"] = df["Total onboard"].astype(int)
df ["Passengers onboard"]= df["Passengers onboard"].astype(int)
df ["Crew onboard"]= df["Crew onboard"].astype(int)
df ["Total dead"]= df["Total dead"].astype(int)
df ["Passengers dead"]= df["Passengers dead"].astype(int)
df ["Crew dead"]= df["Crew dead"].astype(int)
#%%

tot_surv_column = df["Total onboard"] - df["Total dead"]
pas_surv_column = df["Passengers onboard"] - df["Passengers dead"]
crew_surv_column = df["Crew onboard"] - df["Crew dead"]


df["Total survivors"] = tot_surv_column
df["Passengers survivors"] = pas_surv_column
df["Crew survivors"] = crew_surv_column



#%%
# Trim out invalid splits on number of people onboard aircraft

df['error'] = np.where((df['Total onboard'] >= (df['Passengers onboard'] + df['Crew onboard']))
                     , 'valid', 'invalid')

df = df[df.error == 'valid']
df = df.drop(columns=['error'])

#%%
# Split colum Date into Date and Month

df[['Month','Date']] = df.Date.str.split(' ', expand = True)

#%%
# Save wrangled dataset.

df.to_csv('crashes_to_visualize.csv')