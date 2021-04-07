# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 02:06:12 2021

@author: Tarandeep
"""

import pandas as pd
import numpy as np
import time

#format of input ({Location}, {SKU})
#preferred format ({Row}, {Column}, {a/b}, {SKU})

def orderLineDivision (specs, storeOrderDict, skuAssignment): #skuAssignment is dataframe
    #array has now been moved at the top so all order lines for all stores can be compiled here

    
    """
    Update: for loop was added, as this was only one dataframe before (now multiple)
    This for loop will loop through all dataframes in the dictionary, where every df is for a seperate store 
    on the same day.
    """
    
    completedOrderLines = []
    
    weight = specs[['SAP #','Case Volume (cuft)']]
    maxVolume = 80 #assumtion made at 48"x40"x6' 
    
    for date, storeOrder in storeOrderDict.items():
        

        
        dayOrderLines = []
        

        for key, pickList in storeOrder.items():
            
            skuAssignment.sort_values(['Row','Column'], inplace=True) #inplace of old dataframe
            
            """
            will take in the skus to be picked and their quantity, and create lists of skus to be picked that wil be used for calculating distance
            will assume a weight of 80 cuft for now, to be changed
            
            """
            
            
            pickList = pickList.merge(weight, left_on='SKU', right_on='SAP #')
            if (pickList.empty==False):
                pickList = pickList.drop(columns=['SAP #'])
                pickList = pickList.merge(skuAssignment, how='left') #issue with merge on unique values, creates duplicates
                pickList['Total Volume'] = pickList['Quantity']*pickList['Case Volume (cuft)']
                pickList = pickList.sort_values(by=['Column','Row'], ascending=True) #sort by columns (the aisles) and rows (locations in the rows)
                pickList.reset_index(inplace=True, drop=True)
                
                temp = 0
                count = 1     
                appendList = []
                for row in pickList.itertuples():
                    if ((row[7]+temp)>maxVolume): #row[11] is the 12th element in the tuple - THIS CAN CHANGE! CAREFUL ADDING/REMOVING COLUMNS IN DF
                        count+=1
                        temp = 0 + row[7]
                        appendList.append(count)
                    else: 
                        temp = temp + row[7]
                        appendList.append(count)        
                pickList['Order Line'] = appendList
                #convert to tuples for distance algorithm
                
                for i in range(0,np.int_(pickList['Order Line'].max())):
                    empty_array = []
                    df = pickList[pickList['Order Line']==(i+1)] #starts at 0, but order line starts at 1
                    for index in df.index:
                        empty_array.append((df['Row'][index],df['Column'][index]))
                    dayOrderLines.append(empty_array)
            else:
                pass
            #print("Picklist for store " + str(key) + " have been completed.")
        completedOrderLines.append(dayOrderLines)
        print("Picklists for " + str(date) + " have been completed.")
        #print("Store " + str(key) + " order pick lines have been created.")
    print("All store order pick lines have been created.")
    return completedOrderLines
