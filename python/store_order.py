# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 02:12:33 2021

@author: Tarandeep
"""

import pandas as pd

"""
This will take the order lines and compile into useable format to create pick lists.
Store orders are compiled as seperate dictionaries, so towmotors don't pick orders for multiple stores on the same pallet.
"""
def storeOrderComp(storeOrderList):
    
    #storeOrderList = storeOrderList[storeOrderList['Date facture'] == orderDate]
    storeOrderList = storeOrderList.rename(columns={"Article":"SKU", "Delivery Quantity":"Quantity"})
    storeOrderList = storeOrderList.drop(["SU","Delivery", "Date facture"], axis=1)
    
    #slice data frame based on all stores
    #https://stackoverflow.com/questions/19790790/splitting-dataframe-into-multiple-dataframes
    
    allStores = storeOrderList['Ship-to'].unique()
    orderListDict = {elem: pd.DataFrame for elem in allStores}
    for key in orderListDict.keys():
        orderListDict[key] = storeOrderList[:][storeOrderList['Ship-to'] == key]
        orderListDict[key] = orderListDict[key].drop(["Ship-to"], axis=1).reset_index().drop(["index"], axis=1)
    return orderListDict