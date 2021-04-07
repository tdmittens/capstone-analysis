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
    
    orderDictWithDates = {}
    storeOrderList = storeOrderList.rename(columns={"Article":"SKU", "Delivery Quantity":"Quantity"})
    storeOrderList['Date facture'] = storeOrderList['Date facture'].dt.strftime('%m/%d/%Y')
    uniqueDates = storeOrderList['Date facture'].unique().tolist()
    uniqueDates.sort()
    count = 0 #TODO temp
    for orderDate in uniqueDates:
        storeOrderByDate = storeOrderList[storeOrderList['Date facture'] == orderDate]
        
        allStores = storeOrderByDate['Ship-to'].unique()
        orderListDict = {elem: pd.DataFrame for elem in allStores}
        for key in orderListDict.keys():
            orderListDict[key] = storeOrderByDate[:][storeOrderByDate['Ship-to'] == key]
            orderListDict[key] = orderListDict[key].drop(["Ship-to"], axis=1).reset_index().drop(["index"], axis=1)
        orderDictWithDates[orderDate] = orderListDict
        print("Store order for " +  str(orderDate) + " is complete.")
        count+=1 #TODO temp
        if count>3: break #TODO temp
    return orderDictWithDates