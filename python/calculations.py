# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:06 2021

@author: Tarandeep

This file contains calculations for each of the heuristics used in our model, 
    and will assign SKUs based off distance (for weight/COI), and by ABC assignment for ABC model

"""

import pandas as pd
import numpy as np
from sklearn.utils import shuffle
#from order_lines import orderLineComp
import math


availSpaces = 1541*2
ABCfreq = (0.5, 0.8, 1)

# random heuristic


def randomAssignment(specs):
    # r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx
    compiled_data_df = pd.DataFrame()
    specs = shuffle(specs)
    specs.reset_index(inplace=True, drop=True)
    specs.reset_index(inplace=True, drop=False)
    compiled_data_df['SAP #'] = specs['SAP #']
    compiled_data_df['Index'] = specs.index
    return compiled_data_df

# COI heuristic


def coiAssignment(specs, pickFrequency):
    compiled_data_df = pd.DataFrame()
    compiled_data_df = specs.merge(
        pickFrequency, left_on='SAP #', right_on='Article')
    compiled_data_df['COI'] = compiled_data_df['average'] / \
        compiled_data_df['Number of pick pallets (vi)']
    compiled_data_df = compiled_data_df.sort_values(by=['COI'], ascending=True)
    compiled_data_df = compiled_data_df[['SAP #', 'COI']]
    return compiled_data_df


# Weight heuristic
def weightAssignment(specs):
    compiled_data_df = pd.DataFrame()
    compiled_data_df['SAP #'] = specs['SAP #']
    compiled_data_df['Weight'] = specs['Case Weight (kg)'] / \
        specs['Case Volume (cuft)']
    compiled_data_df = compiled_data_df.sort_values(
        by=['Weight'], ascending=False)
    compiled_data_df = compiled_data_df[['SAP #', 'Weight']]
    return compiled_data_df

# ABC heuristic


def abcAssignment(specs):
    specs = specs.sort_values(by=['Restocks'], ascending=False)
    specs['cumsum'] = specs['Number of pick pallets (vi)'].cumsum()
    specs = specs.drop(['Number of pick pallets (vi)'], axis=1)
    return specs


# space allocation import


def spaceAllocationMultiply(SKUList, SpaceAllocation):
    compiled_data_df = SKUList.merge(
        SpaceAllocation, left_on='SAP #', right_on='SAP #')
    returnFrame = pd.DataFrame()
    for index in compiled_data_df.index:
        count = np.int_(compiled_data_df['Number of pick pallets (vi)'][index])
        row = compiled_data_df.xs(index)
        for i in range(count):
            returnFrame = returnFrame.append(row)
    returnFrame.reset_index(inplace=True, drop=True)
    return returnFrame

# SKU assignment


def SKUAssignment(locationDistances, assignment):
    #df = locationDistances.sort_values(by=['Distance'], ascending=True)
    append_df = assignment['SAP #']
    df = locationDistances.join(append_df)
    df.rename(columns={'SAP #':'SKU'}, inplace=True)
    return df

# def ABCAssignment(locationDistance, assignment, abcType:string):
#    if abcType is 'across':
