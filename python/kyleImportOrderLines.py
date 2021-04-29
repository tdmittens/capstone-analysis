# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:48:03 2021

@author: Tarandeep
"""

import numpy as np

def kyleOrderLines (orders):
    completedOrderLines = []

    # convert to tuples for distance algorithm

    for i in range(0, np.int_(orders['Order'].max())):
        empty_array = []
        for index in df.index:
            empty_array.append(
                (df['Row'][index], df['Column'][index]))
        dayOrderLines.append(empty_array)

        completedOrderLines.append(dayOrderLines)
    print("All store order pick lines have been created.")