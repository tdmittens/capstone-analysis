# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:29:19 2021

@author: Tarandeep
"""

def distanceCalculation(distanceNodes):
    distance = 0
    
    #params
    BETWEEN = 5.89 #travel along aisles
    LOWERVERT = 68.87 #below crossaisle
    UPPERVERT = 52.25 #above crossaisle
    
    
    prevNode = distanceNodes[0]
    for node in distanceNodes:
        if node == prevNode:
            pass
        #if moving along aisles
        elif node[1] == prevNode[1]: 
            distance += BETWEEN
        #if moving from middle to north
        elif prevNode[0] == 1 and node[0] == 2: 
            distance += UPPERVERT
        #if moving from middle to south
        elif prevNode[0] == 1 and node[0] == 0:
            distance += LOWERVERT
        #if moving from south to middle - note that cross aisles already checked before above
        elif prevNode[0] == 0:
            distance += LOWERVERT
        elif prevNode[0] ==2:
            distance += UPPERVERT
        prevNode = node

    return distance