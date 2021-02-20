"""
Before creating web app, this will serve as main file for all calculations

"""
import pandas as pd

from layout import layoutDistance
from order_lines import orderLineComp
from calculations import randomAssignment, coiAssignment, weightAssignment, abcAcrossAssignment, abcHorAssignment, SKUAssignment
from order_division import orderLineDivision
from distance_algo import sortIntoAisles, bottomNode, middleNode, topNode, distanceAlgo

# file location decl.

orderLinesLocation = 'D:\OneDrive - Ryerson University\Kyle Files'

# dataframe decl.
layout = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\final_layout.xlsx')
specs = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')
pickList = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\test\Pick List Test.xlsx')
storeOrder = pd.read_excel(r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\test\Pick List Test.xlsx')

# additional variables
availSpaces = 1541*2
ABCfreq = (0.5, 0.8, 1)

# determine distance for each pick spot
locationDistance = layoutDistance(layout)

# compile order lines together
#pickFrequency = orderLineComp(orderLinesLocation)

# calculate assignments using all methods & divide store orders
randomOrderLines = orderLineDivision (specs, storeOrder, pickList, SKUAssignment(locationDistance, randomAssignment(specs)))
coiOrderLines = orderLineDivision (specs, storeOrder, pickList, SKUAssignment(locationDistance, coiAssignment(specs, pickFrequency)))
weightOrderLines = orderLineDivision (specs, storeOrder, pickList, SKUAssignment(locationDistance, weightAssignment(specs)))
#abcHorizOrderLines = orderLineDivision (specs, storeOrder, pickList, SKUAssignment(locationDistance, abcHorAssignment(specs))
#abcVertiOrderLines = orderLineDivision (specs, storeOrder, pickList, SKUAssignment(locationDistance, abcAcrossAssignment(specs))

# calculate distance for each method




# export data into excel sheets



