# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:30:04 2021

@author: Tarandeep
"""

"""
Method will use sales data dataframe
"""

import pandas as pd

def salesDataComp (salesDataDict):
    returnFrame = pd.DataFrame(columns=["SKU", "Description", "Total"])
    for key, df in salesDataDict.items(): #value is the dataframe in this case=
        if key == list(salesDataDict.keys())[0]: #first sheet should not be merged, https://www.geeksforgeeks.org/python-get-the-first-key-in-dictionary/
            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
            returnFrame["SKU"] = df["5"]
            returnFrame["Description"] = df["6"]
            returnFrame["Total"] = df[str(len(df.columns))]
            returnFrame = returnFrame.dropna().reset_index(drop=True)
        else:
            df.columns = [str(x) for x in range(1,len(df.columns)+1)]
            emptyFrame = pd.DataFrame(columns=["SKU", "Total"])
            emptyFrame["SKU"] = df["5"]
            emptyFrame["Total"] = df[str(len(df.columns))]
            emptyFrame = emptyFrame.dropna()
            returnFrame = returnFrame.merge(emptyFrame, on="SKU") #inner join of df
    returnFrame['Grand Total'] = returnFrame.iloc[:,2:].sum(axis=1)
    returnFrame = returnFrame[['SKU','Description','Grand Total']]
    return returnFrame
    