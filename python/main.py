"""
Before creating web app, this will serve as main file for all calculations

"""
import pandas as pd
import math

from layout import layoutDistance
from order_lines import orderLineComp
from calculations import randomAssignment, coiAssignment, weightAssignment, abcAcrossAssignment, abcHorAssignment, SKUAssignment, spaceAllocationMultiply
from order_division import orderLineDivision
from distance_algo import distanceAlgo
from gui import gui_method
from distance_calc import distanceCalculation
from space_allocation import spaceAllocation
from sales_data import salesDataComp

# run gui

gui_values = gui_method()
layout = pd.read_excel(gui_values['layout'])
specs = pd.read_excel(gui_values['specs'])
#pickList = gui_values['pickList']
storeOrder = pd.read_excel(gui_values['storeOrder'])
pickList = pd.read_excel(gui_values['storeOrder'])
orderLinesLocation = gui_values['orderLinesLocation']

# sales data needs to be a list of multiple dataframes (one dataframe for each year)
# this will create dictionary of all sheets
salesDataDict = pd.read_excel(gui_values['salesData'], None)
salesDataFrame = salesDataComp(salesDataDict)

# space allocation
spaceAllocation = spaceAllocation(specs)

# additional variables
availSpaces = 1541*2
ABCfreq = (0.5, 0.8, 1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]
aisleTuple = (1,23,52)

# determine distance for each pick spot
locationDistance = layoutDistance(layout)

# compile order lines together
#   pickFrequency = orderLineComp(orderLinesLocation)
pickFrequency = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\python\order_lines_df.xlsx')


# random
if gui_values['random'] == True:
    randomSKU = SKUAssignment(
        locationDistance, randomAssignment(specs))  # sku assignment
    # calculate assignment and divide store orders
    randomOrderLines = orderLineDivision(
        specs, storeOrder, pickList, randomSKU)
    randomDistance = []  # distance for each towmotor
    for orderLine in randomOrderLines:  # calculate distance for each towmotor
        randomDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# coi
if gui_values['coi'] == True:
    coiAsgn = coiAssignment(specs, pickFrequency)
    coiSKU = SKUAssignment(
        locationDistance, coiAssignment(specs, pickFrequency))
    coiSKU2 = spaceAllocationMultiply(
        coiAssignment(specs, pickFrequency), spaceAllocation)
    coiOrderLines = orderLineDivision(specs, storeOrder, pickList, coiSKU)
    coiDistance = []
    for orderLine in coiOrderLines:
        coiDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# weight
if gui_values['weight'] == True:
    weightSKU = SKUAssignment(locationDistance, weightAssignment(specs))
    weightOrderLines = orderLineDivision(
        specs, storeOrder, pickList, weightSKU)
    weightDistance = []
    for orderLine in weightOrderLines:
        weightDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet

# abc horizontal
if gui_values['across'] == True:
    #abcHorizSKU= SKUAssignment(locationDistance, abcHorAssignment(specs, ABCcutoff))
    #abcHorizOrderLines = orderLineDivision (specs, storeOrder, pickList, abcHorizSKU)
    abcHDistance = []
    for orderLine in abcHorizOrderLines:
        abcHDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet


# abc vertical
if gui_values['vertical'] == True:
    #abcVertiSKU= SKUAssignment(locationDistance, abcAcrossAssignment(specs, ABCcutoff))
    #abcVertiOrderLines = orderLineDivision (specs, storeOrder, pickList, abcVertiSKU)
    abcVDistance = []
    for orderLine in abcVertiOrderLines:
        abcVDistance.append(distanceCalculation(distanceAlgo(orderLine)))
    pass  # export into excel sheet
