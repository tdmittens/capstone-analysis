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
    specs = pd.read_excel(gui_values['specs'])
else:
    print("Specifications file not specified. Default file will be used.")
    specs = pd.read_excel(r"default\SKU Info.xlsx")

# store orders/pick list

if gui_values['storeOrder'] != "":
    storeOrderData = pd.read_excel(gui_values['storeOrder'])
else:
    print("Store order file not specified. Default file will be used.")
    storeOrderData = pd.read_excel(r"default\sample order line.xlsx")

"""
This block of code will be used to compile order lines together. 
If no file location is added, a default file will be used.
"""
orderLinesLocation = gui_values['orderLinesLocation']
if (orderLinesLocation != ""):
    pickFrequency = orderLineComp(orderLinesLocation)
else:
    print("No path has been loaded in to compile order lines. A default generated file will be used in this case.")
    pickFrequency = pd.read_excel(r'default\order_lines_df.xlsx')

# Sales data
if gui_values['salesData'] != "":
    salesDataDict = pd.read_excel(gui_values['salesData'], None)
else:
    print("Sales data not specified. Default file will be used.")
    salesDataDict = pd.read_excel(r"default\Sales Data.xlsx", None)

# export path
if gui_values['exportLocation'] != "":
    exportLocation = gui_values['exportLocation']
else:
    print("Export location not specified. ../python/export will be used as path ")
    exportLocation = r"export"

# store order date
if gui_values['salesYear'] == "" or gui_values['salesMonth'] == "" or gui_values['salesDay'] == "":
    print("One of the fields are missing. Default day of 05/11/2020 will be used.")
    orderDate = "5/11/2020"
else:
    orderDate = gui_values['salesMonth'] + "/" + \
        gui_values['salesDay'] + "/" + gui_values['salesYear']

# Tuple for week range
try:
    weekRange = ((int)(gui_values['startWeek']), (int)(gui_values['endWeek']))
except:
    print("Provided week range has not been provided or is not a number. Default range of week 27-35 will be used.")
    weekRange = (27, 35)

"""
Store orders must be compiled to be for a specific date, divided into multiple data frames for each store
This will return back a dictionary of data frames with every data frame being one store
"""

pickListDict = storeOrderComp(storeOrderData)

"""
This will take the specifications file and modify it for use in VBA model and future use cases
"""

specs = specsDataComp(specs, salesDataDict, weekRange)

"""
Determine the distance for each pick spot
"""
locationDistance = layoutDistance(layout)


"""
This will import the data to an Excel File to use OpenSolver
Lastly, it will return a dataframe with SpaceAllocation
"""
if gui_values['spaceAllocate'] == True:
    if gui_values['maxSpaces'] != "":
        maxSpaces = (int)(gui_values['maxSpaces'])
    else:
        print("Value not entered. Max spaces set to 8.")
        maxSpaces = 1

    spaceAllocationTable = excelApp(specs,
                                    r"default\space_allocation.xlsm",
                                    maxSpaces,
                                    # total spaces in layout distance dataframe
                                    len(locationDistance.index),
                                    len(specs.index))  # amount of SKUS in current specs table
else:
    spaceAllocationTable = spaceAllocationDataFrame(
        r"default\space_allocation.xlsm")
    print("Space allocation model did not run. Previous model will be used instead.")
    print("Total spaces set to 2688.")
    totalSpaces = 10

# add space allocation to specs dataframe
specs = specsAddSpaceAllocation(specs, spaceAllocationTable)

"""
This will set the aisle tuple based off inputs given by user
"""

aisleTuple = (1, 1, 3)
if gui_values['aisleTop'] == "" or gui_values['aisleMiddle'] == "" or gui_values['aisleBottom'] == "":
    print("One of the cross aisles are missing. The default values of 1, 24, 52 will be used.")
    
else:
    try:
        aisleTuple = ((int)(gui_values['aisleTop']), (int)(
            gui_values['aisleMiddle']), (int)(gui_values['aisleBottom']))
    except:
        print("Inputs for cross aisles are invalid. The The default value of 1, 24, 52 will be used.")

# additional variables
availSpaces = len(locationDistance.index)
ABCfreq = (0.5, 0.8, 1)
ABCcutoff = [math.floor(availSpaces * x) for x in ABCfreq]


"""
This block of code will implement SKU allocation models, dependant if the user selected them in the GUI.
It will also determine the minimum distance taken for each of the models as well.
For each heuristic, it will also compile a visual layout of where SKUs are in the facility.
Once all assignments and distance evaluations are completed, these SKUS will be exported into a file
This will require SKU Assignment, Order Lines, and Total Distance for all Order Lines
"""

"""
UPDATE: Import orders 

"""
orders = pd.read_excel(r"kyleFiles\orders.xlsx")

# random
if gui_values['random'] == True:
    print("Random process has now started.")
    randomSKU = pd.read_excel(r"kyleFiles\randomSkuAssignment.xlsx")
    randomOrderLines = orderLineDivision(specs, orders, randomSKU)
    
    randomDistancePeriod = []
    for orderLine in randomOrderLines:
        if len(orderLine)>0:
            randomDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine, aisleTuple)))
    
    randomVisualSKU = visualSKUOutput(randomSKU, aisleTuple)
    exportFiles(randomSKU, randomVisualSKU, randomOrderLines,
                randomDistancePeriod, exportLocation, "random")

# super cool KYLE SKU assignment - popularity
if gui_values['coi'] == True:
    print("Super cool Kyle SKU popularity process has now started.")
    coiSKU = pd.read_excel(r"kyleFiles\popSkuAssignment.xlsx")
    coiOrderLines = orderLineDivision(specs, orders, coiSKU)

    coiDistancePeriod = []
    coiAllDistanceNodes = []
    for orderLine in coiOrderLines:
        if len(orderLine)>0:
            coiDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine, aisleTuple)))
            coiAllDistanceNodes.append(distanceAlgo(orderLine, aisleTuple))

    coiVisualSKU = visualSKUOutput(coiSKU, aisleTuple)
    exportFiles(coiSKU, coiVisualSKU, coiOrderLines,
                coiDistancePeriod, exportLocation, "popularity")

# super cool KYLE SKU assignment - interaction freq.
if gui_values['weight'] == True:
    print("Super cool Kyle SKU interaction process has now started.")
    weightSKU = pd.read_excel(r"kyleFiles\interactionSkuAssignment.xlsx")
    weightOrderLines = orderLineDivision(specs, orders, weightSKU)
    
    
    weightDistancePeriod = []
    for orderLine in weightOrderLines:
        if len(orderLine)>0:
            weightDistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine, aisleTuple)))
        

    weightVisualSKU = visualSKUOutput(weightSKU, aisleTuple)
    exportFiles(weightSKU, weightVisualSKU, weightOrderLines,
                weightDistancePeriod, exportLocation, "interaction")

#additional layout 1
    print("Super cool Kyle SKU layout 1 process has now started.")
    lay1SKU = pd.read_excel(r"kyleFiles\lay1SkuAssignment.xlsx")
    lay1OrderLines = orderLineDivision(specs, orders, lay1SKU)
    
    
    lay1DistancePeriod = []
    for orderLine in lay1OrderLines:
        if len(orderLine)>0:
            lay1DistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine, aisleTuple)))
        

    lay1VisualSKU = visualSKUOutput(lay1SKU, aisleTuple)
    exportFiles(lay1SKU, lay1VisualSKU, lay1OrderLines,
                lay1DistancePeriod, exportLocation, "layout1")

#additional layout 2
    print("Super cool Kyle SKU layout 2 process has now started.")
    lay2SKU = pd.read_excel(r"kyleFiles\lay2SkuAssignment.xlsx")
    lay2OrderLines = orderLineDivision(specs, orders, lay2SKU)
    
    
    lay2DistancePeriod = []
    for orderLine in lay2OrderLines:
        if len(orderLine)>0:
            lay2DistancePeriod.append(distanceCalculation(
                distanceAlgo(orderLine, aisleTuple)))
        

    lay2VisualSKU = visualSKUOutput(lay2SKU, aisleTuple)
    exportFiles(lay2SKU, lay2VisualSKU, lay2OrderLines,
                lay2DistancePeriod, exportLocation, "layout2")

# abc horizontal
if gui_values['across'] == True:
    print("ABC Across aisle assignment process has now started.")
    horizLocation = orderByHorizontal(locationDistance, aisleTuple)
    abcHorizSKU = SKUAssignment(horizLocation, spaceAllocationMultiply(
        abcAssignment(specs), spaceAllocationTable))
    abcHorizOrderLines = orderLineDivision(specs, pickListDict, abcHorizSKU)

    abcHDistancePeriod = []

    for dailyOrder in abcHorizOrderLines:
        abcHDistance = []
        for orderLine in dailyOrder:
            abcHDistanceNodes = distanceCalculation(
                distanceAlgo(orderLine, aisleTuple))
            abcHDistance.append(abcHDistanceNodes)
        abcHDistancePeriod.append(abcHDistance)

    abcHorizVisualSKU = visualSKUOutput(abcHorizSKU, aisleTuple)
    exportFiles(abcHorizSKU, abcHorizVisualSKU, abcHorizOrderLines,
                abcHDistancePeriod, exportLocation, "across")


# abc vertical
if gui_values['vertical'] == True:
    print("ABC Vertical aisle assignment process has now started.")
    vertiLocation = orderByVertical(locationDistance, aisleTuple)
    abcVertiSKU = SKUAssignment(vertiLocation, spaceAllocationMultiply(
        abcAssignment(specs), spaceAllocationTable))
    abcVertiOrderLines = orderLineDivision(specs, pickListDict, abcVertiSKU)

    abcVDistancePeriod = []
    abcVDistanceNodes = []

    for dailyOrder in abcVertiOrderLines:
        abcVDistance = []
        for orderLine in dailyOrder:
            abcVDistanceNode = distanceAlgo(orderLine, aisleTuple)
            abcVDistanceNodes.append(abcVDistanceNode)
            abcVDistance.append(distanceCalculation(abcVDistanceNode))
        abcVDistancePeriod.append(abcVDistance)

    abcVertiVisualSKU = visualSKUOutput(abcVertiSKU, aisleTuple)
    exportFiles(abcVertiSKU, abcVertiVisualSKU, abcVertiOrderLines,
                abcVDistancePeriod, exportLocation, "vertical")


# exportDistancesOnly(randomDistancePeriod, coiDistancePeriod, weightDistancePeriod,
#                     exportLocation)
evaluationFile(randomDistancePeriod, coiDistancePeriod, weightDistancePeriod,lay1DistancePeriod, lay2DistancePeriod, exportLocation)


print("All heuristic methods have been completed and results have been exported.")
"""
This code block will run the final evaluation model to compare the different models
"""


print("Analysis is now complete.")
