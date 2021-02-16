# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:06 2021

@author: Tarandeep
"""

import pandas as pd
from sklearn.utils import shuffle
#from order_lines import orderLineComp
import math


#space allocation import

availSpaces = 1541*2
ABCfreq = (0.5,0.8,1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]

space_allocation_df = pd.DataFrame()

# random heuristic

specs = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')

specs = shuffle(specs)
specs.reset_index(inplace=True, drop=True)

# COI heuristic

specs2 = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')

orderLinesdf = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\python\order_lines_df.xlsx', index_col=0)

#orderLinesdf = orderLineComp()
#orderLinesdf.to_excel("order_lines_df.xlsx")

compiled_data_df = pd.DataFrame()
compiled_data_df = specs2.merge(
    orderLinesdf, left_on='SAP #', right_on='Article')

compiled_data_df['COI'] = compiled_data_df['average'] / \
    compiled_data_df['Number of pick pallets (vi)']

# Weight heuristic

compiled_data_df['Weight'] = compiled_data_df['Case Weight (kg)'] / \
    compiled_data_df['Case Volume (cuft)']

# ABC heuristic

abc_df = pd.DataFrame()

specs2 = specs2.sort_values(by=['Restocks'], ascending = False)
specs2['cumsum'] = specs2['Number of pick pallets (vi)'].cumsum()

#SKU assignment


##abc_df['location'] = (specs2['cumsum'] < ABCcutoff[0])
#abc_df['A'] = specs2['SAP #'][specs2['cumsum'] < ABCcutoff[0]]
#abc_df['B'] = specs2['SAP #'][(specs2['cumsum'] < ABCcutoff[1]) & (specs2['cumsum'] > ABCcutoff[0])]
#abc_df['C'] = specs2['SAP #'][specs2['cumsum'] > ABCcutoff[1]]


