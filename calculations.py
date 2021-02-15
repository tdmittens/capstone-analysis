# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:06 2021

@author: Tarandeep
"""

import pandas as pd
from sklearn.utils import shuffle
from order_lines import orderLineComp

orderLinesNeeded = False

#random heuristic

specs = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')

specs = shuffle(specs)
specs.reset_index(inplace=True, drop=True) 

#COI heuristic

specs2 = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')

if orderLinesNeeded == True:
    orderLinesdf = orderLineComp()

compiled_data_df = pd.DataFrame()
compiled_data_df = specs2.merge(orderLinesdf, left_on='SAP #', right_on='Article')
                       
compiled_data_df['COI'] = compiled_data_df['average']/compiled_data_df['Number of pick pallets (vi)']

#Weight heuristic

compiled_data_df['Weight'] = compiled_data_df['Case Weight (kg)']/compiled_data_df['Case Volume (cuft)']

#ABC heuristic

