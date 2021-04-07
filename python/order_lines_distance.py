# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:20:25 2021
@author: Tarandeep
"""

import pandas as pd
import glob
import os
#from tkinter.filedialog import askdirectory

def orderLineDistance (orderLinesLocation):
    #filename = askdirectory()
    
    # ref: https://stackoverflow.com/questions/11295917/how-to-select-a-directory-and-store-the-location-using-tkinter-in-python
    # use your path
    all_files = glob.glob(os.path.join(orderLinesLocation, "*.xlsx"))     # advisable to use os.path.join as this makes concatenation OS independent
    
    
    #for f in all_files:
    #    df_from_each_file = []
    #    df = pd.read_excel(f)
    #    df_from_each_file.append(df)
    #    print ("complete")
        
    print("Compiling Files...")
    df_from_each_file = (pd.read_excel(f) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    print("File Compilation Complete!")
    with pd.ExcelWriter(r"D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\python\export\order_lines_distance.xlsx", engine='xlsxwriter') as writer:
        concatenated_df.to_excel(writer, sheet_name='Sample order line new')
    return concatenated_df
    
#    num_years = 2.0
#    
#    count_df = concatenated_df.groupby(["Article"], as_index = False).size().reset_index(name='counts')
#    count_df["average"] = round(count_df["counts"]/num_years,0)
#    return count_df
    
