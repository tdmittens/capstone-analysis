"""
Before creating web app, this will serve as main file for all calculations

"""
import pandas as pd
import math

from layout import layoutDistance, orderByVertical, orderByHorizontal
from order_lines import orderLineComp
from calculations import randomAssignment, coiAssignment, weightAssignment, abcAssignment, SKUAssignment, spaceAllocationMultiply
from order_division import orderLineDivision
from distance_algo import distanceAlgo
from gui import gui_method
from distance_calc import distanceCalculation
from space_allocation import excelApp, spaceAllocationDataFrame
from sales_data import specsDataComp, specsAddSpaceAllocation  # ,salesDataComp
from export import exportFiles, visualSKUOutput, evaluationFile, exportDistancesOnly
from store_order import storeOrderComp

"""
This code block will run GUI and retrieve all paths for all files
These files will then be imported as Excel Files
Update: Try and except block have been removed 
"""

gui_values = gui_method()

"""
This will run a new GUI which will show all Console results
Update: Debug window will be depreciated, as executable will use console instead
"""

#sg.Print('Re-routing print to debug window.', do_not_reroute_stdout=False)


# layout

if gui_values['layout'] != "":
    layout = pd.read_excel(gui_values['layout'])
else:
    print("Layout file not specified. Default file will be used.")
    layout = pd.read_excel(r"default\final_layout.xlsx")

# specs

if gui_values['specs'] != "":
    pickList = pd.read_excel(gui_values['specs'])
else:
    print("Picklist file not specified. Default file will be used.")
    pickList = pd.read_excel(r"default\SKU Info.xlsx")

"""
UPDATE: Import orders 

"""
if gui_values['orders'] != "":
    orders = pd.read_excel(gui_values['orders'])
else:
    print("Orders file not specified. Default file will be used.")
    orders = pd.read_excel(r"kyleFiles\orders.xlsx")


# export path
if gui_values['exportLocation'] != "":
    exportLocation = gui_values['exportLocation']
else:
    print("Export location not specified. ../python/export will be used as path ")
    exportLocation = r"export"
    

"""
Determine the distance for each pick spot
"""
locationDistance = layoutDistance(layout)


"""
This will set the aisle tuple based off inputs given by user
"""
# aisleTuple = (1, 1, 3)
# if gui_values['aisleTop'] == "" or gui_values['aisleMiddle'] == "" or gui_values['aisleBottom'] == "":
#     print("One of the cross aisles are missing. The default values of 1, 1, 3 will be used.")
    
# else:
#     try:
#         aisleTuple = ((int)(gui_values['aisleTop']), (int)(
#             gui_values['aisleMiddle']), (int)(gui_values['aisleBottom']))
#     except:
#         print("Inputs for cross aisles are invalid. The The default value of 1, 1, 3 will be used.")

# additional variables
availSpaces = len(locationDistance.index)
ABCfreq = (0.5, 0.8, 1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]

"""
Text entries for each of the SKUs
"""
if gui_values['sku1Text'] != "":
    sku1Text = gui_values['sku1Text']
else:
    sku1Text = "SKU 1"

if gui_values['sku2Text'] != "":
    sku2Text = gui_values['sku2Text']
else:
    sku2Text = "SKU 2"
    
if gui_values['sku3Text'] != "":
    sku3Text = gui_values['sku3Text']
else:
    sku3Text = "SKU 3"
    
if gui_values['sku4Text'] != "":
    sku4Text = gui_values['sku4Text']
else:
    sku4Text = "SKU 4"
    
if gui_values['sku5Text'] != "":
    sku5Text = gui_values['sku5Text']
else:
    sku5Text = "SKU 5"

"""
This block of code will implement SKU allocation models, dependant if the user selected them in the GUI.
It will also determine the minimum distance taken for each of the models as well.
For each heuristic, it will also compile a visual layout of where SKUs are in the facility.
Once all assignments and distance evaluations are completed, these SKUS will be exported into a file
This will require SKU Assignment, Order Lines, and Total Distance for all Order Lines
"""



#sku1
if gui_values['sku1'] == True:
    print("Process for SKU Assignment 1 has started.")
    randomSKU = pd.read_excel(r"kyleFiles\randomSkuAssignment.xlsx")
    randomOrderLines = orderLineDivision(pickList, orders, randomSKU)
    
    randomDistancePeriod = []
    for orderLine in randomOrderLines:
        if len(orderLine)>0:
            randomDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine)))
    
    randomVisualSKU = []
    exportFiles(randomSKU, randomVisualSKU, randomOrderLines,
                randomDistancePeriod, exportLocation, sku1Text)

#sku2
if gui_values['sku2'] == True:
    print("Process for SKU Assignment 2 has started.")
    coiSKU = pd.read_excel(r"kyleFiles\popSkuAssignment.xlsx")
    coiOrderLines = orderLineDivision(pickList, orders, coiSKU)

    coiDistancePeriod = []
    coiAllDistanceNodes = []
    for orderLine in coiOrderLines:
        if len(orderLine)>0:
            coiDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine)))
            coiAllDistanceNodes.append(distanceAlgo(orderLine))

    coiVisualSKU = []
    exportFiles(coiSKU, coiVisualSKU, coiOrderLines,
                coiDistancePeriod, exportLocation, sku2Text)

#sku3
if gui_values['sku3'] == True:
    print("Process for SKU Assignment 3 has started.")
    weightSKU = pd.read_excel(r"kyleFiles\interactionSkuAssignment.xlsx")
    weightOrderLines = orderLineDivision(pickList, orders, weightSKU)
    
    
    weightDistancePeriod = []
    for orderLine in weightOrderLines:
        if len(orderLine)>0:
            weightDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine)))
        

    weightVisualSKU = []
    exportFiles(weightSKU, weightVisualSKU, weightOrderLines,
                weightDistancePeriod, exportLocation, sku3Text)

#sku4
if gui_values['sku4'] == True:
    print("Process for SKU Assignment 4 has started.")
    lay1SKU = pd.read_excel(r"kyleFiles\lay1SkuAssignment.xlsx")
    lay1OrderLines = orderLineDivision(pickList, orders, lay1SKU)
    
    
    lay1DistancePeriod = []
    for orderLine in lay1OrderLines:
        if len(orderLine)>0:
            lay1DistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine)))
        

    lay1VisualSKU = []
    exportFiles(lay1SKU, lay1VisualSKU, lay1OrderLines,
                lay1DistancePeriod, exportLocation, sku4Text)

#sku 5
if gui_values['sku5'] == True:
    print("Process for SKU Assignment 5 has started.")
    lay2SKU = pd.read_excel(r"kyleFiles\lay2SkuAssignment.xlsx")
    lay2OrderLines = orderLineDivision(pickList, orders, lay2SKU)
    
    
    lay2DistancePeriod = []
    for orderLine in lay2OrderLines:
        if len(orderLine)>0:
            lay2DistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine)))
        

    lay2VisualSKU = []
    exportFiles(lay2SKU, lay2VisualSKU, lay2OrderLines,
                lay2DistancePeriod, exportLocation, sku5Text)


# exportDistancesOnly(randomDistancePeriod, coiDistancePeriod, weightDistancePeriod,
#                     exportLocation)
evaluationFile(randomDistancePeriod, coiDistancePeriod, weightDistancePeriod,lay1DistancePeriod, lay2DistancePeriod, exportLocation)


print("All heuristic methods have been completed and results have been exported.")
"""
This code block will run the final evaluation model to compare the different models
"""


print("Analysis is now complete.")
