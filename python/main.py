"""
Before creating web app, this will serve as main file for all calculations

"""


from layout import layoutDistance
from order_lines import orderLinesComp
from calculations import randomAssignment, coiAssignment, weightAssignment, abcAcrossAssignment, abcHorAssignment, SKUAssignment
from order_division import orderLineDivision
from distance_algo import sortIntoAisles, bottomNode, middleNode, topNode, distanceAlgo



# determine distance for each pick spot
locationDistance = layoutDistance(
    'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\Programming Models\Final Capstone Model (w git)\capstone-analysis\final_layout.xlsx')

# compile order lines together


# calculate assignments using all methods



#



# divide store order into delivery lines



# calculate distance for each method