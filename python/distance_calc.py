# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:29:19 2021

@author: Tarandeep


This is a method used after the distance algorithm is commplete
This will take the nodes traversed and convert to distance
"""


def distanceCalculation(distanceNodes):
    distance = 0

    # params
    BETWEEN = 144  # travel along aisles
    LOWERVERT = 0  # below crossaisle
    UPPERVERT = 40  # above crossaisle

    prevNode = distanceNodes[0]
    for node in distanceNodes:
        if node == prevNode:
            pass
        # if moving along aisles
        elif node[1] == prevNode[1]:
            distance += BETWEEN
        # if moving from middle to north
        # elif prevNode[0] == 1 and node[0] == 2:
        #     distance += UPPERVERT
        # # if moving from middle to south
        # elif prevNode[0] == 1 and node[0] == 0:
        #     distance += LOWERVERT
        # if moving from south to middle - note that cross aisles already checked before above
        elif prevNode[0] == 0:
            distance += UPPERVERT
        elif prevNode[0] == 1:
            distance += UPPERVERT
        prevNode = node

    return distance
