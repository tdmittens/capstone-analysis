# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:30 2021

@author: Tarandeep
"""

#import cplex
#from doopl.factory import create_opl_model
#import pandas as pd
#
#
## data import
#specs = pd.read_excel(
#    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')
#
#flow = specs['fi'].tolist()
#volume = specs['Volume/ pallet (cu ft)'].tolist()
#
#n = 1541
#
#
#with create_opl_model(model="Space Allocation.mod") as opl:
#    opl.set_input("flow", flow)
#    opl.set_input("volume1", flow)
#    opl.run()
#    report = opl.report

import pandas as pd
import win32com.client
import os, os.path
import time

def excelApp(specs, inputPath, SpacesPerSKU:int, TotalSpaces:int, TotalSKUs:int, exportPath):
    ExcelApp = win32com.client.Dispatch("Excel.Application")
    ExcelApp.Visible = True
    
    #create new workbook
    ExcelWorksheet = ExcelApp.Workbooks.Open(inputPath)
    ExcelSheet = ExcelWorksheet.WorkSheets("Sheet1")
    
    #reconfigure specifications file
    
    specs = specs[['SAP #', 'Ti', 'Hi', '# items/time period']]
    
    #set specificiations into excel file
    #https://stackoverflow.com/questions/22469054/write-a-data-frame-to-worksheet-using-win32com-in-python
    StartRow = 2
    StartCol = 1
    ExcelSheet.Range(ExcelSheet.Cells(StartRow,StartCol),# Cell to start the "paste"
         ExcelSheet.Cells(StartRow+len(specs.index)-1,
                  StartCol+len(specs.columns)-1)
         ).Value = specs.values
    
    #assign locations based off layout of excel sheet
    loc1 = ExcelWorksheet.Worksheets("Sheet1").Range("Q2")
    loc2 = ExcelWorksheet.Worksheets("Sheet1").Range("Q4")
    loc3 = ExcelWorksheet.Worksheets("Sheet1").Range("Q6")
    
    #assign value to locations
    loc1.value = SpacesPerSKU 
    loc2.value = TotalSpaces
    loc3.value = TotalSKUs 
    
    
    #ExcelApp.Application.Run(inputPath + "!Sheet4.setupsolver")
    #ExcelWorksheet.SaveAs(Filename=exportPath)
    #try catch for Space allocation macro
    try:
        ExcelApp.Application.Run(os.path.basename(inputPath)+"!Module5.setupsolver")
    except:
        print("Space Allocation Macro is not working, please confirm OpenSolver is installed on Microsoft Excel, and ensure Opensolver is enabled in VBA References. Check out https://opensolver.org/installing-opensolver/ to download.")
    
    #try catch for saving file
    try:
        ExcelWorksheet.Save()
    except:
        print("File could not be saved. Please try again.")
    
    
    #this will create async process that will wait for file to quit before continuing
    #update - async unreliable, add finite time delay for now
        
    ExcelApp.Application.Quit()
    print("Waiting for file to close...")
    time.sleep(10)
    space_allocation_df = pd.read_excel(inputPath, "Solver Sheet")
    space_allocation_df.drop(0,inplace=True)
    space_allocation_df.drop(space_allocation_df.columns[0:7],axis=1,inplace=True)
    space_allocation_df.drop(space_allocation_df.columns[3:5],axis=1,inplace=True)
    space_allocation_df.columns = ["SAP #","Zij","Number of pick pallets (vi)"]
    return space_allocation_df
    
    #set reference to range of cells
    
#run function
    
#ExcelApp(specs = pd.read_excel(),
#         r"D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\python\space_allocation.xlsm",
#         8,
#         2688,
#         1541,
#         r"D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\python\space_allocation_2.xlsm")
    
