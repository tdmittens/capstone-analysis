"""
This file contains all distance calculations and serves as the evaluation model


For reference:
    
Every SKU has the format (r,c) where r is the horizonatl location, and c is the vertical location
Every node has the format (h,v) where h is every horizontal aisle, and v is erery vertical aisle
"""


# imports

from operator import itemgetter

# this method will take the SKUList and convert SKUS to aisle numbers for picks


def sortIntoAisles(SKUList):
    # SKU = (2,7) where 2 is aisle, 7 is location
    newSKUList = []
    for SKU in SKUList:
        if SKU[1] % 2 == 0:
            SKUAisle = SKU[1]/2
        else:
            SKUAisle = int(SKU[1]/2)+1
        newSKU = (SKU[0], SKUAisle)
        newSKUList.append(newSKU)

    # https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
    newSKUList.sort(key=itemgetter(1))
    return newSKUList

# this method is just to check if it should enter the current aisle on its tour or keep moving forward in the bottom aisle

# def flipStartPoint(SortedList, LastAisle):
#    for SKU in SortedList:
#        SKU[0] = (LastAisle+1)-SKU[0]


def bottomNode(dataTuple, sorted, lastAisle):
    # if at last aisle
    if dataTuple[1] == lastAisle:
        return (dataTuple)

    # if aisle cannot be entered
    if dataTuple[1] % 2 == 0:
        return (dataTuple[0], dataTuple[1]+1)

    for SKU in sorted:
        # only need one sku to move in that direction
        if SKU[1] == dataTuple[1] or SKU[1] == dataTuple[1]+1:
            return (dataTuple[0]+1, dataTuple[1])
    # if none are true, towmotor can move to next aisle
    return (dataTuple[0], dataTuple[1]+1)


# def middleNode(dataTuple, sorted, aisles, lastAisle):
#     # if at last aisle
#     if dataTuple[1] == lastAisle:
#         return (dataTuple[0]-1, dataTuple[1])

#     if dataTuple[1] % 2 == 1:  # moving in upwards direction
#         for SKU in sorted:
#             if (SKU[1] == dataTuple[1] and SKU[0] >= aisles[1]):
#                 return (dataTuple[0]+1, dataTuple[1])
#             elif (SKU[1] == dataTuple[1]+1 and SKU[0] >= aisles[1]):
#                 return (dataTuple[0]+1, dataTuple[1])
#         return (dataTuple[0], dataTuple[1]+1)
#     else:  # moving in downwards direction
#         for SKU in sorted:
#             # will look at skus below cross aisle
#             if (SKU[0] == dataTuple[1] and SKU[0] < aisles[1]):
#                 return (dataTuple[0]-1, dataTuple[1])
#             elif (SKU[0] == dataTuple[1]+1 and SKU[0] < aisles[1]):
#                 return (dataTuple[0]-1, dataTuple[1])
#         return (dataTuple[0], dataTuple[1]+1)


def topNode(dataTuple, sorted, lastAisle):
    # if at last aisle
    if dataTuple[1] == lastAisle:
        return (dataTuple[0]-1, dataTuple[1])

    # if aisle cannot be entered
    if dataTuple[1] % 2 == 1:
        return (dataTuple[0], dataTuple[1]+1)

    for SKU in sorted:
        # only need one sku to move in that direction
        if SKU[1] == dataTuple[1] or SKU[1] == dataTuple[1]+1:
            return (dataTuple[0]-1, dataTuple[1])

    return (dataTuple[0], dataTuple[1]+1)


def distanceAlgo(SKUList):
    SKUComplete = False
    sortedList = sortIntoAisles(SKUList)  # sort SKUS in order
    lastAisle = (sortedList[len(sortedList)-1])[1]

    # this condition will ensure that the picker can leave the warehouse when complete
    
    if lastAisle % 2 == 1:
        lastAisle += 1
    
#    sortedList = flipStartPoint(sortedList, lastAisle) #bandaid to flip sku pick locations

    # current node will be a tuple
    # tuple starts at
    currentNode = (0, (sortedList[0])[1]-1)
#    if currentNode[1] <= 0:
#        currentNode = (0,lastAisle)
    allNodes = [currentNode]

    while (SKUComplete is False):
        #    if currentNode[0]>lastAisle: #need to fix, should be done through method
        #        break
        if currentNode[0] == 0:
            currentNode = bottomNode(currentNode, sortedList, lastAisle)
        # elif currentNode[0] == 1:
        #     currentNode = middleNode(
        #         currentNode, sortedList, aisles, lastAisle)
        elif currentNode[0] == 1:
            currentNode = topNode(currentNode, sortedList, lastAisle)
        if currentNode == (0, lastAisle):
            SKUComplete = True
        allNodes.append(currentNode)
        # print(currentNode)

    return allNodes

#    print(allNodes)
#    # just temp print out of pathing
#    for node in allNodes:
#        emptyPath[2-node[1]][node[0]-1] = 1
#
#    # https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
#    print('\n'.join([''.join(['{:2}'.format(item) for item in row])
#                     for row in emptyPath]))
