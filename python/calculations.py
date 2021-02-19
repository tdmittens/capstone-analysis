# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:06 2021

@author: Tarandeep

This file contains calculations for each of the heuristics used in our model, 
    and will assign SKUs based off distance (for weight/COI), and by ABC assignment for ABC model

"""

import pandas as pd
from sklearn.utils import shuffle
#from order_lines import orderLineComp
import math


# space allocation import

availSpaces = 1541*2
ABCfreq = (0.5, 0.8, 1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]

# random heuristic
def randomAssignment(specsFilePath):
    specs = pd.read_excel(specsFilePath)
    #r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx
    specs = shuffle(specs)
    specs.reset_index(inplace=True, drop=True)
    return specs

# COI heuristic
def coiAssignment(specsFilePath, orderLinesFilePath):
    specs = pd.read_excel(specsFilePath)
    #r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx'
    orderLinesdf = pd.read_excel(orderLinesFilePath, index_col=0)
    #r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\python\order_lines_df.xlsx', index_col=0

    compiled_data_df = pd.DataFrame()
    compiled_data_df = specs.merge(orderLinesdf, left_on='SAP #', right_on='Article')

    compiled_data_df['COI'] = compiled_data_df['average'] / compiled_data_df['Number of pick pallets (vi)']
    return compiled_data_df


# Weight heuristic
def weightAssignment(specsFilePath, orderLinesFilePath):
    specs = pd.read_excel(specsFilePath)
    #r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx'
    orderLinesdf = pd.read_excel(orderLinesFilePath, index_col=0)
    #r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\python\order_lines_df.xlsx', index_col=0

    compiled_data_df = pd.DataFrame()
    compiled_data_df = specs.merge(orderLinesdf, left_on='SAP #', right_on='Article')
    compiled_data_df['Weight'] = compiled_data_df['Case Weight (kg)'] / \
    compiled_data_df['Case Volume (cuft)']
    return compiled_data_df

# ABC heuristic
def abcAcrossAssignment(specsFilePath):
    specs = pd.read_excel(specsFilePath)
    compiled_data_df = pd.DataFrame()
    specs = specs.sort_values(by=['Restocks'], ascending=False)
    specs['cumsum'] = specs['Number of pick pallets (vi)'].cumsum()

def abcHorAssignment(specsFilePath):
    specs = pd.read_excel(specsFilePath)
    compiled_data_df = pd.DataFrame()
    specs = specs.sort_values(by=['Restocks'], ascending=False)
    specs['cumsum'] = specs['Number of pick pallets (vi)'].cumsum()

#SKU assignment



