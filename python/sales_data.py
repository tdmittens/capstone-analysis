# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:30:04 2021

@author: Tarandeep
"""

"""
Method will use sales data dataframe
Update: Sales Data will only use FY2019 and FY2020 to maintain consistency between data frames
"""

import pandas as pd
import numpy as np

#def salesDataComp (salesDataDict):
#    returnFrame = pd.DataFrame(columns=["SKU", "Description", "Total"])
#    for key, df in salesDataDict.items(): #value is the dataframe in this case=
#        if key == list(salesDataDict.keys())[0]: #first sheet should not be merged, https://www.geeksforgeeks.org/python-get-the-first-key-in-dictionary/
#            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
#            returnFrame["SKU"] = df["5"]
#            returnFrame["Description"] = df["6"]
#            returnFrame["Total"] = df[str(len(df.columns))]
#            returnFrame = returnFrame.dropna().reset_index(drop=True)
#        else:
#            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
#            emptyFrame = pd.DataFrame(columns=["SKU", "Total"])
#            emptyFrame["SKU"] = df["5"]
#            emptyFrame["Total"] = df[str(len(df.columns))]
#            emptyFrame = emptyFrame.dropna()
#            returnFrame = returnFrame.merge(emptyFrame, on="SKU") #inner join of df
#    returnFrame['Grand Total'] = returnFrame.iloc[:,2:].sum(axis=1)
#    returnFrame = returnFrame[['SKU','Description','Grand Total']]
#    return returnFrame

def specsDataComp (specs, salesDataDict, weekRange):
    #returnFrame = pd.DataFrame(columns=["SKU", "Description", "Items/Time Period", "Total"])
    returnFrame = pd.DataFrame()
    for key, df in salesDataDict.items(): #value is the dataframe in this case=
        #first sheet should not be merged, and should be created to be merged on
        #https://www.geeksforgeeks.org/python-get-the-first-key-in-dictionary/
        if key == list(salesDataDict.keys())[0]: 
            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
            df.drop(df.index[[0,1,2,3,4]],inplace=True)
            df.drop(df[df["5"] == "Result"].index, inplace=True)
            df = df.replace(np.nan,0)
            returnFrame["SKU"] = df["5"]
            returnFrame["Description"] = df["6"]
            for i in range(weekRange[0]+6,weekRange[1]+6+1):
                returnFrame["Week " + str(i-6)] = df[str(i+6)].astype('float64')
        else:
            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
            df.drop(df.index[[0,1,2,3,4]],inplace=True)
            df.drop(df[df["5"] == "Result"].index, inplace=True)
            df = df.replace(np.nan,0)
            emptyFrame = pd.DataFrame()
            emptyFrame["SKU"] = df["5"]
            #emptyFrame["Description"] = df["6"]
            for i in range(weekRange[0]+6,weekRange[1]+6+1):
                emptyFrame["Week " + str(i-6)] = df[str(i+6)].astype('float64')
            returnFrame = returnFrame.merge(emptyFrame, on='SKU', how='right') #right merge so only 2020 skus are added
            #returnFrame = pd.merge(left=returnFrame, right=emptyFrame, left_on='SKU', right_on='SKU')
            #returnFrame = returnFrame.merge(emptyFrame, how='inner', on="SKU") #inner join of df
    #returnFrame['Grand Total'] = returnFrame.iloc[:,2:].sum(axis=1)
    #returnFrame = returnFrame[['SKU','Description','Grand Total']]
    returnFrame['# items/time period'] = returnFrame.sum(axis=1, numeric_only=True)
    returnFrame['# items/time period'] = returnFrame['# items/time period']/(weekRange[1]-weekRange[0])
    returnFrame['SKU'] = returnFrame['SKU'].astype('int64')
    returnFrame = returnFrame[['SKU','# items/time period']]
    specs = specs.merge(returnFrame, left_on="SAP #", right_on="SKU", how='left')
    specs.drop(['SKU'], axis=1, inplace=True)
    specs = specs.replace(np.nan,0)
    specs = specs[specs['# items/time period']!=0] #to ensure there is at least one item moving in two years
    return specs

def specsAddSpaceAllocation (specs, spaceAllocation):
    spaceAllocation = spaceAllocation[['SAP #','Number of pick pallets (vi)']]
    specs = specs.merge(spaceAllocation, left_on='SAP #', right_on='SAP #', how='inner')
    specs['Items/Pallet'] = specs['Ti']*specs['Hi']
    specs['Flow'] = specs['# items/time period']/specs['Items/Pallet']
    specs['Restocks'] = specs['Flow']/specs['Number of pick pallets (vi)']
    #specs.drop(['SAP #'], axis=1, inplace=True)
    return specs