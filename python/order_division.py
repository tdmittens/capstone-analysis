# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 02:06:12 2021

@author: Tarandeep
"""

import pandas as pd
import numpy as np

#format of input ({Location}, {SKU})
#preferred format ({Row}, {Column}, {a/b}, {SKU})

def orderLineDivision (specs, storeOrder, pickList, skuAssignment): #skuAssignment is dataframe

    #new_df = pd.DataFrame(columns = ["Row", "Column", "A/B", "SKU"])
    weight = specs[['SAP #','Case Volume (cuft)']]
    
    #new_df["A/B"] = skuAssignment["Location"].str[-1]
    #new_df["Column"] = pd.to_numeric(skuAssignment["Location"].str[-3:-1])
    #new_df["Row"] = pd.to_numeric(skuAssignment["Location"].str[:-3])
    #new_df["SKU"] = skuAssignment["SKU"]
    
    skuAssignment.sort_values(['Row','Column'], inplace=True) #inplace of old dataframe
    
    """
    will take in the skus to be picked and their quantity, and create lists of skus to be picked that wil be used for calculating distance
    will assume a weight of 200 kg for now, to be changed
    
    """
    
    maxWeight = 80 #assumtion made at 48"x40"x6' = 
    pickList = pickList.merge(weight, left_on='SKU', right_on='SAP #')
    pickList = pickList.drop(columns=['SAP #'])
    pickList = pickList.merge(skuAssignment, how='left') #issue with merge on unique values, creates duplicates
    pickList['Total Volume'] = pickList['Quantity']*pickList['Case Volume (cuft)']
    pickList['Order Line'] = np.nan
    pickList = pickList.sort_values(by=['Column','Row'], ascending=True) #sort by columns (the aisles) and rows (locations in the rows)
    pickList.reset_index(inplace=True, drop=True)
    
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
#    for index in pickList.index:
#        completedOrderLines[pickList['Order Line']].append((pickList['Row'],pickList['Column']))
    
    
    for i in range(0,np.int_(pickList['Order Line'].max())):
        empty_array = []
        df = pickList[pickList['Order Line']==(i+1)] #starts at 0, but order line starts at 1
        for index in df.index:
            empty_array.append((df['Row'][index],df['Column'][index]))
#        for index, row in df.iterrows():
#            empty_array.append((row['Row'],row['Column']))
        completedOrderLines.append(empty_array)
        
    return completedOrderLines
    #return pickList

#pickList['Weight'] = pickList.lookup(pickList['SKU'], specs['Case Weight (kg)']) 
#    