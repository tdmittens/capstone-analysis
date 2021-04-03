# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 20:53:53 2021

@author: Tarandeep
"""

import numpy as np
import pandas as pd


"""
This function will take SKU assignment and present it in a visual form that
will be exported to an Excel sheet for use by company
"""
def visualSKUOutput (SKUAssignment, aisleTuple):
    
    #Aisle tuple - start aisles at 0 instead of 1
    #https://stackoverflow.com/questions/17418108/elegant-way-to-perform-tuple-arithmetic
    aisleTuple = tuple(np.subtract(aisleTuple, (1,1,1)))
    
    #obtain list of columns in SKU Assignment
    listColumns = SKUAssignment['Column'].unique().tolist()
    listColumns.sort()
    
    #create empty 2D array
    array = [["" for i in range((np.int_(SKUAssignment['Column'].max()))*3)] for j in range(aisleTuple[len(aisleTuple)-1])]
    
    counter = 0
    for colNo in range(0,np.int_(SKUAssignment['Column'].max())):
        #if column has skus, do something
        if colNo in listColumns:
            #this will find the index of the column in this list, useful to determine if print...
            #should be done on left hand side or right hand side
            actualCol = listColumns.index(colNo)
            #if column is even
            if actualCol%2 != 0:
                for rowNo in range(aisleTuple[0], aisleTuple[len(aisleTuple)-1]):
                    if rowNo in aisleTuple and rowNo != 0:
                        array[rowNo][counter] = "X"
                        array[rowNo][counter+1] = "X"
                        array[rowNo][counter+2] = "X"
                    else:
                        #create dataframe that is only
                        df = SKUAssignment.loc[(SKUAssignment['Row']==rowNo) & (SKUAssignment['Column']==colNo)]
                        if df.empty:
                            pass #keep cells empty
                        else:
                            array[rowNo][counter] = df.loc[df['A/B'] == 'A'].iloc[0]['SKU']
                            array[rowNo][counter+1] = df.loc[df['A/B'] == 'B'].iloc[0]['SKU']
                            #https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
                            array[rowNo][counter+2] = "{:02d}".format(actualCol+1) + "{:02d}".format(rowNo+1) #+1 to start from 1 instead of 0
                counter+=3
            #if column is odd
            else:     
                for rowNo in range(aisleTuple[0], aisleTuple[len(aisleTuple)-1]):
                    if rowNo in aisleTuple and rowNo != 0: #update: rowNo!=0 added to omit aisle at top of excel sheet, as it overlapped SKUs in row 1
                        array[rowNo][counter] = "X"
                        array[rowNo][counter+1] = "X"
                        array[rowNo][counter+2] = "X"
                    else:
                        #create dataframe that is only
                        df = SKUAssignment.loc[(SKUAssignment['Row']==rowNo) & (SKUAssignment['Column']==colNo)]
                        if df.empty:
                            pass #keep cells empty
                        else:
                            array[rowNo][counter+2] = df.loc[df['A/B'] == 'A'].iloc[0]['SKU']
                            array[rowNo][counter+1] = df.loc[df['A/B'] == 'B'].iloc[0]['SKU']
                            #https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
                            array[rowNo][counter] = "{:02d}".format(actualCol+1) + "{:02d}".format(rowNo+1) #+1 to start from 1 instead of 0
                counter+=3
        #if column is not in list, just fill entire column with X
        else:
            for rowNo in range(0, aisleTuple[len(aisleTuple)-1]):
                array[rowNo][counter] = "X"
            counter+=1
    return array

"""
This will create a file to view for each heuristic
"""
def exportFiles(assignmentSKU, visualSKU:list, orderLines, orderDistance, exportPath:str, heuristicType:str):
    
    path = exportPath + "/" + heuristicType + ".xlsx"
    
    visual_sku_df = pd.DataFrame(visualSKU)
    order_lines_df = pd.DataFrame(orderLines).T
    order_distance_df = pd.DataFrame(orderDistance)
    
    """
    SKU assignment should have the correct columns 
    """
    
    #obtain list of columns in SKU Assignment
    listColumns = assignmentSKU['Column'].unique().tolist()
    listColumns.sort()
    
    #fix column numbers
    for colNo in range(0,np.int_(assignmentSKU['Column'].max())):
        if colNo in listColumns:
            actualCol = listColumns.index(colNo)
            assignmentSKU.loc[assignmentSKU['Column'] == colNo, 'Column'] = actualCol+1
            
    #sort by column and reset index
    assignmentSKU = assignmentSKU.sort_values(['Column', 'Row'], ascending=True).reset_index(drop=True)
        
    #https://xlsxwriter.readthedocs.io/example_pandas_multiple.html
    #https://stackoverflow.com/questions/62618680/overwrite-an-excel-sheet-with-pandas-dataframe-without-affecting-other-sheets
    """
    This will delete workbook to ensure file is completely overwritten
    """
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
#        workBook = writer.book
#        try:
#            workBook.remove()
#            print("Old workbook has been removed.")
#        except:
#            print("Workbook does not exist and cannot be deleted. New workbook will be created.")
#        finally:
            assignmentSKU.to_excel(writer, sheet_name='SKU Assignment')
            visual_sku_df.to_excel(writer, sheet_name='SKU Layout')
            order_lines_df.to_excel(writer, sheet_name='Order Line Pick Up')
            order_distance_df.to_excel(writer, sheet_name='Order Line Distances')
            print("The file for " + heuristicType + " has been compiled. It has been saved to " + path)
            # Close the Pandas Excel writer and output the Excel file.
            writer.save()

"""
This will evaluate the different models based off what is decided (distributions, % comparison, etc...)
"""
def evaluationFile():
    pass





#file = exportFiles(randomSKU, "", "", (1,23,52))