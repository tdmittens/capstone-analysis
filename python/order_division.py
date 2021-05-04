# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 02:06:12 2021

@author: Tarandeep
"""

import pandas as pd
import numpy as np
import time

# format of input ({Location}, {SKU})
# preferred format ({Row}, {Column}, {a/b}, {SKU})


def orderLineDivision(orders, skuAssignment):  # skuAssignment is dataframe
    # array has now been moved at the top so all order lines for all stores can be compiled here
    """
    Update: for loop was added, as this was only one dataframe before (now multiple)
    This for loop will loop through all dataframes in the dictionary, where every df is for a seperate store 
    on the same day.
    """

    completedOrderLines = []

    # inplace of old dataframe
    skuAssignment.sort_values(['Row', 'Column'], inplace=True)

    """
    will take in the skus to be picked and their quantity, and create lists of skus to be picked that wil be used for calculating distance
    will assume a weight of 80 cuft for now, to be changed
    
    """
    

    if (skuAssignment.empty == False):
        # issue with merge on unique values, creates duplicates
        pickList = skuAssignment.sort_values(
            by=['Column', 'Row'], ascending=True)
        pickList.reset_index(inplace=True, drop=True)
        
    
        for i in range(0, np.int_(pickList['Order'].max())):
            empty_array = []
            # starts at 0, but order line starts at 1
            df = pickList[pickList['Order'] == (i+1)]
            for index in df.index:
                empty_array.append(
                    (pickList['Row'][index], pickList['Column'][index]))
            completedOrderLines.append(empty_array)

    print("All store order pick lines have been created.")
    return completedOrderLines
