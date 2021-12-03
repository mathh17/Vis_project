# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:10:10 2021''

@author: jakob
"""
#import libraries
import pandas as pd

#Load data
df = pd.read_excel('crashes.xlsx')

#Drop columns of no interest
df = df.drop(columns="Registration")
df = df.drop(columns="Cn_ln")

#Split colum 'route' and create two new 'from', 'to'
df[['To', 'From']] = df['Route'].str.split(' - ', 1, expand=True)
#split month and data 'Date' into 'Month' and 'Date'--last replacing the origin
df[['Month', 'Date']] = df['Date'].str.split(' ', 1, expand=True)



