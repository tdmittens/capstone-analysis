# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:45:52 2021

@author: Tarandeep
"""

# ref https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog


import pandas as pd
import numpy as np

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

    # fix column numbers
    listColumns = locations_df['Column'].unique().tolist()
    listColumns.sort()

    for colNo in range(0, np.int_(locations_df['Column'].max())+1):
        if colNo in listColumns:
            actualCol = listColumns.index(colNo)
            locations_df.loc[locations_df['Column']
                             == colNo, 'Column'] = actualCol+1

    return locations_df


def orderByVertical(locationDistance, aisles):
    locationDistance = locationDistance.sort_values(
        by=['Column', 'Row'], ascending=False)
    returnFrame = pd.DataFrame()
    # create loop to append in increments of 10
    counter = aisles[2]
    increment = 10
    while counter > increment:
        returnFrame = returnFrame.append(
            locationDistance[locationDistance['Row'] > counter])
        locationDistance = locationDistance.drop(
            locationDistance[locationDistance['Row'] > counter].index, axis=0)
        counter -= increment
    returnFrame = returnFrame.append(locationDistance)
    returnFrame = returnFrame.reset_index(drop=True)

#    df1 = locationDistance[locationDistance['Row']>aisles[1]]
#    df2 = locationDistance[locationDistance['Row']<aisles[1]]
#    returnFrame = df1.append(df2, ignore_index = True)
    return returnFrame


def orderByHorizontal(locationDistance, aisles):
    # sort by aisle, then by row, starting from bottom and working to the top
    returnFrame = locationDistance.sort_values(
        by=['Column', 'Row'], ascending=False)
    returnFrame = returnFrame.reset_index(drop=True)
    return returnFrame
