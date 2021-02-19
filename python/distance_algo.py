"""


"""


# imports

from operator import itemgetter


# this method will take the SKUList and convert SKUS to aisle numbers for picks


def sortIntoAisles(SKUList):
    # SKU = (2,7) where 2 is aisle, 7 is location
    newSKUList = []
    for SKU in SKUList:
        SKUAisle = int((SKU[0]/2)+1)  # will not round
        newSKU = (SKUAisle, SKU[1])
        newSKUList.append(newSKU)

    # https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
    newSKUList.sort(key=itemgetter(0))
    return newSKUList

# this method is just to check if it should enter the current aisle on its tour or keep moving forward in the bottom aisle


def bottomNode(dataTuple, sorted, lastAisle):
    # if at last aisle
    if dataTuple[0] == lastAisle:
        return (dataTuple)

    # if aisle cannot be entered
    if dataTuple[0] % 2 == 0:
        return (dataTuple[0]+1, dataTuple[1])

    for SKU in sorted:
        # only need one sku to move in that direction
        if SKU[0] == dataTuple[0] or SKU[0] == dataTuple[0]+1:
            return (dataTuple[0], dataTuple[1]+1)
    # if none are true, towmotor can move to next aisle
    return (dataTuple[0]+1, dataTuple[1])


def middleNode(dataTuple, sorted, aisles, lastAisle):
    # if at last aisle
    if dataTuple[0] == lastAisle:
        return (dataTuple[0], dataTuple[1]-1)

    if dataTuple[0] % 2 == 1:  # moving in upwards direction
        for SKU in sorted:
            if (SKU[0] == dataTuple[0] and SKU[1] < aisles[1]):
                return (dataTuple[0], dataTuple[1]+1)
            elif (SKU[0] == dataTuple[0]+1 and SKU[1] < aisles[1]):
                return (dataTuple[0], dataTuple[1]+1)
        return (dataTuple[0]+1, dataTuple[1])
    else:  # moving in downwards direction
        for SKU in sorted:
            # will look at skus below cross aisle
            if (SKU[0] == dataTuple[0] and SKU[1] >= aisles[1]):
                return (dataTuple[0], dataTuple[1]-1)
            elif (SKU[0] == dataTuple[0]+1 and SKU[1] >= aisles[1]):
                return (dataTuple[0], dataTuple[1]-1)
        return (dataTuple[0]+1, dataTuple[1])


def topNode(dataTuple, sorted, lastAisle):
    # if at last aisle
    if dataTuple[0] == lastAisle:
        return (dataTuple[0], dataTuple[1]-1)

    # if aisle cannot be entered
    if dataTuple[0] % 2 == 1:
        return (dataTuple[0]+1, dataTuple[1])

    for SKU in sorted:
        # only need one sku to move in that direction
        if SKU[0] == dataTuple[0] or SKU[0] == dataTuple[0]+1:
            return (dataTuple[0], dataTuple[1]-1)

    return (dataTuple[0]+1, dataTuple[1])

def distanceAlgo(SKUList):
    SKUComplete = False
    #locationDataFrame = None
    SKUList = [(1, 3), (6, 2), (14, 4), (11, 42),  (18, 4), (23, 23),
               (5, 38), (29, 7)]  # input - locations of skus
    
    
    sortedList = sortIntoAisles(SKUList)  # sort SKUS in order
    #sortedList = [(1, 3), (4, 38), (6,2), (8,2), (10, 4), (12, 4), (13, 23)]
    aisles = [0, 23, 51]  # based off excel sheet
    lastAisle = (sortedList[len(sortedList)-1])[0]
    emptyPath = [[0 for i in range(lastAisle)]for j in range(3)]
    
    # current node will be a tuple, that will be replaced in function location
    currentNode = (0, 0)
    allNodes = []
    
    while (SKUComplete is False):
        #    if currentNode[0]>lastAisle: #need to fix, should be done through method
        #        break
        if currentNode[1] == 0:
            currentNode = bottomNode(currentNode, sortedList, lastAisle)
        elif currentNode[1] == 1:
            currentNode = middleNode(currentNode, sortedList, aisles, lastAisle)
        elif currentNode[1] == 2:
            currentNode = topNode(currentNode, sortedList, lastAisle)
        if currentNode == (lastAisle, 0):
            SKUComplete = True
        allNodes.append(currentNode)
        # print(currentNode)
    
    print(allNodes)
    # just temp print out of pathing
    for node in allNodes:
        emptyPath[2-node[1]][node[0]-1] = 1
    
    # https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
    print('\n'.join([''.join(['{:2}'.format(item) for item in row])
                     for row in emptyPath]))

    
