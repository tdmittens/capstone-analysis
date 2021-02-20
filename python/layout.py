# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:45:52 2021

@author: Tarandeep
"""

# ref https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog


import pandas as pd

"""
This will take layout and compile distance for every location

"""
def layoutDistance(layout_df):
    
    locations_df = pd.DataFrame(columns=["Row", "Column", "A/B", "Distance"])

    for i in range(0, len(layout_df)):
        for j in range(0, len(layout_df.columns)):
            locations_df = locations_df.append(
                {'Row': i+1, 'Column': j+1, 'A/B': 'A', 'Distance': layout_df.iloc[i, j]}, ignore_index=True)
            locations_df = locations_df.append(
                {'Row': i+1, 'Column': j+1, 'A/B': 'B', 'Distance': layout_df.iloc[i, j]}, ignore_index=True)
    
    locations_df = locations_df.dropna()
    locations_df = locations_df.sort_values(by=['Distance'], ascending=True)
    locations_df.reset_index(inplace=True, drop=True)

    return locations_df