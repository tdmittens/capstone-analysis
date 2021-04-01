"""
Before creating web app, this will serve as main file for all calculations

"""
import pandas as pd
import math
import PySimpleGUI as sg

from layout import layoutDistance, orderByVertical, orderByHorizontal
from order_lines import orderLineComp
from calculations import randomAssignment, coiAssignment, weightAssignment, abcAssignment, SKUAssignment, spaceAllocationMultiply
from order_division import orderLineDivision
from distance_algo import distanceAlgo
from gui import gui_method
from distance_calc import distanceCalculation
from space_allocation import excelApp
from sales_data import salesDataComp, specsDataComp
#from export import exportFiles

"""
This code block will run GUI and retrieve all paths for all files
These files will then be imported as Excel Files
Update: Try and except block have been removed 
"""

gui_values = gui_method()

"""
This will run a new GUI which will show all Console results
"""

sg.Print('Re-routing print to debug window.', do_not_reroute_stdout=False)


#layout

if gui_values['layout'] != "":
    layout = pd.read_excel(gui_values['layout'])
else:
    print("Layout file not specified. Default file will be used.")
    layout = pd.read_excel(r"default\final_layout.xlsx")
    
#specs

if gui_values['specs'] != "":
    specs = pd.read_excel(gui_values['specs'])
else:
    print("Specifications file not specified. Default file will be used.")
    specs = pd.read_excel(r"default\SKU Info.xlsx")
    
#store orders/pick list

if gui_values['storeOrder'] != "":
    pickList = pd.read_excel(gui_values['storeOrder'])
else:
    print("Store order file not specified. Default file will be used.")
    pickList = pd.read_excel(r"default\sample order line.xlsx")
    
"""
This block of code will be used to compile order lines together. 
If no file location is added, a default file will be used.
"""   
orderLinesLocation = gui_values['orderLinesLocation']
if (orderLinesLocation!=""):
    pickFrequency = orderLineComp(orderLinesLocation)
else:
    print("No path has been loaded in to compile order lines. A default generated file will be used in this case.")
    pickFrequency = pd.read_excel(r'default\order_lines_df.xlsx')
        
#Sales data
if gui_values['salesData'] != "":
    salesDataDict = pd.read_excel(gui_values['salesData'], None)
else:
    print("Sales data not specified. Default file will be used.")
    salesDataDict = pd.read_excel(r"default\Sales Data.xlsx", None)

#Tuple for week range
try:  
    weekRange = ((int)(gui_values['startWeek']), (int)(gui_values['endWeek']))
except:
    print("Provided week range has not been provided or is not a number. Default range of week 8-16 will be used.")  
    weekRange = (8,16)

"""
Sales data needs to be a list of multiple dataframes (one dataframe for each year)
This code will create dictionary of all sheets
Update: not needed in this use case scenario, specification file compilation will be done instead
"""

#salesDataFrame = salesDataComp(salesDataDict)

"""
This will take the specifications file and modify it for use in VBA model and future use cases
"""

specs = specsDataComp(specs, salesDataDict, weekRange)

"""
This will import the data to an Excel File to use OpenSolver
Lastly, it will return a dataframe with SpaceAllocation
"""
spaceAllocationTable = excelApp(specs,
         r"default\space_allocation.xlsm",
         8,
         2688,
         1541,
         r"default\space_allocation_2.xlsm")


# additional variables
availSpaces = 1541*2
ABCfreq = (0.5, 0.8, 1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]
aisleTuple = (1,23,52)

# determine distance for each pick spot
locationDistance = layoutDistance(layout)


"""
This block of code will implement SKU allocation models, dependant if the user selected them in the GUI.
It will also determine the minimum distance taken for each of the models as well.
"""

#random
if gui_values['random'] == True:
    randomSKU = SKUAssignment(locationDistance, randomAssignment(specs))  # sku assignment
    # calculate assignment and divide store orders
    randomOrderLines = orderLineDivision(specs, pickList, randomSKU)
    randomDistance = []  # distance for each towmotor
    for orderLine in randomOrderLines:  # calculate distance for each towmotor
        randomDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# coi
if gui_values['coi'] == True:
    #coiAsgn = coiAssignment(specs, pickFrequency)
    coiSKU = SKUAssignment(locationDistance, spaceAllocationMultiply(coiAssignment(specs, pickFrequency), spaceAllocationTable))
    coiOrderLines = orderLineDivision(specs, pickList, coiSKU)
    coiDistance = []
    for orderLine in coiOrderLines:
        coiDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# weight
if gui_values['weight'] == True:
    weightSKU = SKUAssignment(locationDistance, spaceAllocationMultiply(weightAssignment(specs), spaceAllocationTable))
    weightOrderLines = orderLineDivision(specs, pickList, weightSKU)
    weightDistance = []
    for orderLine in weightOrderLines:
        weightDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# abc horizontal
if gui_values['across'] == True:
    horizLocation = orderByHorizontal(locationDistance, aisleTuple)
    abcHorizSKU= SKUAssignment(horizLocation, spaceAllocationMultiply(abcAssignment(specs), spaceAllocationTable))
    abcHorizOrderLines = orderLineDivision (specs, pickList, abcHorizSKU)
    abcHDistance = []
    for orderLine in abcHorizOrderLines:
        abcHDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet


# abc vertical
if gui_values['vertical'] == True:
    vertiLocation = orderByVertical(locationDistance, aisleTuple)
    abcVertiSKU= SKUAssignment(vertiLocation, spaceAllocationMultiply(abcAssignment(specs), spaceAllocationTable))
    abcVertiOrderLines = orderLineDivision (specs, pickList, abcVertiSKU)
    abcVDistance = []
    for orderLine in abcVertiOrderLines:
        abcVDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

"""
Once all assignments and distance evaluations are completed, these SKUS will be exported into a file
This will require SKU Assignment, Order Lines, and Total Distance for all Order Lines
"""
    
#TODO - export files based on layout that Michael gave me


