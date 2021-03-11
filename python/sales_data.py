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
    i=0
    for key, value in salesDataDict.items(): #value is the dataframe in this case
        if key == list(salesDataDict.keys())[0]: #first sheet should not be merged, https://www.geeksforgeeks.org/python-get-the-first-key-in-dictionary/
            returnFrame["SKU"] = value["Unnamed: 4"]
            returnFrame["Description"] = value["Unnamed: 5"]
            returnFrame["Total"] = value["Unnamed: 53"]
            returnFrame = returnFrame.dropna().reset_index(drop=True)
        else:
            emptyFrame = pd.DataFrame(columns=["SKU", "Description", "Total"])
            emptyFrame["SKU"] = value["Unnamed: 4"]
            emptyFrame["Description"] = value["Unnamed: 5"]
            emptyFrame["Total"] = value["Unnamed: 53"]
            emptyFrame = emptyFrame.dropna()
            returnFrame = returnFrame.merge(emptyFrame["SKU","Total"], on="SKU").dropna().reset_index(drop=True) #inner join of df
        i+=1
    return returnFrame
    