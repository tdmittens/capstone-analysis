# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 02:06:12 2021

@author: Tarandeep
"""

import pandas as pd
import numpy as np

#format of input ({Location}, {SKU})
#preferred format ({Row}, {Column}, {a/b}, {SKU})


df = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Pathfinding Algorithm\Test Import File.xlsx')
new_df = pd.DataFrame(columns = ["Row", "Column", "A/B", "SKU"])
specs = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210116 COI Weight Heuristics\210206 Code Updates.xlsm', sheet_name='Average with 2019 uncommon data')
pickList = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Pathfinding Algorithm\Pick List Test.xlsx')
weight = specs[['SAP #','Case Volume (cuft)']]

new_df["A/B"] = df["Location"].str[-1]
new_df["Column"] = pd.to_numeric(df["Location"].str[-3:-1])
new_df["Row"] = pd.to_numeric(df["Location"].str[:-3])
new_df["SKU"] = df["SKU"]

new_df.sort_values(['Row','Column'], inplace=True) #inplace of old dataframe

"""
will take in the skus to be picked and their quantity, and create lists of skus to be picked that wil be used for calculating distance
will assume a weight of 200 kg for now, to be changed

"""

maxWeight = 200
pickList = pickList.merge(weight, left_on='SKU', right_on='SAP #')
pickList = pickList.drop(columns=['SAP #'])
pickList = pickList.merge(new_df, how='left') #issue with merge on unique values, creates duplicates
pickList['Total Volume'] = pickList['Quantity']*pickList['Case Volume (cuft)']
pickList['Order Line'] = np.nan

#temp and count are temp var, for total weight and pick line, resp.
temp = 0
count = 1
for index in pickList.index:
    if (pickList['Total Volume'][index]+temp>maxWeight):
        count+=1
        temp = 0 + pickList['Total Volume'][index]
        pickList['Order Line'][index] = count
    else: 
        temp = temp + pickList['Total Volume'][index]
        pickList['Order Line'][index] = count


#convert to tuples for distance algorithm
completedOrderLines = []
for index in pickList.index:
    completedOrderLines.append((pickList['Row'][index],pickList['Column'][index]))

#pickList['Weight'] = pickList.lookup(pickList['SKU'], specs['Case Weight (kg)']) 
#    
