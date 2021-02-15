# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:45:52 2021

@author: Tarandeep
"""

# ref https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog


import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Tk().withdraw()
#filename = askopenfilename()

filename = r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Python Model\final_layout.xlsx'

layout_df = pd.read_excel(filename)

locations_df = pd.DataFrame(columns=["Row", "Column", "Distance"])

for index, row in layout_df.iterrows():
#    print("index: ", index)
#    print("row: ", row)
    if layout_df.iloc[index,row[index]] != np.nan:
        locations_df.append([row,index,layout_df.iloc[index,row[index]])