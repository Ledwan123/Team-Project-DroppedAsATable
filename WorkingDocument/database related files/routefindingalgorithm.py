from operator import itemgetter
import random

from database_methods import DatabaseMethods

#avg scores of each route

def findRoute(segments, nodes, whereRouting, weightings=None):
    #apply weightings to segments to create a single final weight for each segment
    weightedSegments = []
    if weightings:
        for segment in segments: #apply weightings to each segment
            start, end, length = segment
            weight = length * 2 * weightings[0]
            weightingIterator = 1
            for node in nodes:
                if node[0] == start:
                    for tempWeight in node[1:]:
                        weight += float(tempWeight)*weightings[weightingIterator]
                        weightingIterator+=1
            weightingIterator = 1
            for node in nodes:
                if node[0] == end:
                    for tempWeight in node[1:]:
                        weight += float(tempWeight)*weightings[weightingIterator]
                        weightingIterator+=1
            weightedSegments.append((start, end, weight))
    else:
        for segment in segments: #if no weighting only length is used
            start, end, length = segment
            weight = length
            weightedSegments.append((start, end, weight))

    #sort segments by weight to make priority queue
    sortedSegments = sorted(weightedSegments, key=itemgetter(2)) #sort by segment weight

    #initialize distances dictionary
    distances = {}
    for node in nodes:
        distances[node[0]] = [float('inf')] #distances will start as infinite
    distances[whereRouting[0]] = [0, whereRouting[0]] #distance to starting point is 0
    
    #while there are still segments to process
    while len(sortedSegments) > 0:
        foundSegement = False
        for currentSegment in sortedSegments:
            for currentDistance in distances.values():
                
                #check if current segment connects with last node in the path


                if currentSegment[0] == currentDistance[-1]:
                    newDistance = distances[currentSegment[0]][0] + currentSegment[2]
                    if newDistance < distances[currentSegment[1]][0]: #check if new distance is shorter
                        distances[currentSegment[1]] = [newDistance] + currentDistance[1:] + [currentSegment[1]] #update distance if shorter
                    sortedSegments.remove(currentSegment) #remove segment from queue
                    foundSegement = True
                    break #escape the for loop to restart from beggining of sortedSegments

                elif currentSegment[1] == currentDistance[-1]:
                    newDistance = distances[currentSegment[1]][0] + currentSegment[2]
                    if newDistance < distances[currentSegment[0]][0]: #check if new distance is shorter
                        distances[currentSegment[0]] = [newDistance] + currentDistance[1:] + [currentSegment[0]] #update distance if shorter
                    sortedSegments.remove(currentSegment) #remove segment from queue
                    foundSegement = True
                    break #escape the for loop to restart from beggining of sortedSegments
            
            if foundSegement:
                break #escape the for loop to restart from beggining of sortedSegments
    return distances






def findOtherRoutes(segments, nodes, whereRouting, routes, weightings = [1, 0, 0, 0, 0], seed = 0, similarityNeeded = 30):
    escapeCounter = 0 #escape counter to set max iterations so does not loop forever

    # calculate the total of weightings so that when the weights are adjusted it adjusts them by an apropriate amount
    weightingsMagnitude = 0
    for weight in weightings:
        weightingsMagnitude += weight


    while escapeCounter < 1000:

        #temp values for the weights that are changing to check a weight never goes below 0
        changingWeight1 = -1
        changingWeight2 = -1

        while changingWeight1 < 0 or changingWeight2 < 0:

            #calculate which weight is changing and by how much 
            random.seed(seed)
            whichweight = random.randrange(0, len(weightings))
            random.seed(seed)
            howmuch = random.uniform(0, weightingsMagnitude/10)
            changingWeight1 = weightings[whichweight] + howmuch

            #loop used to iterate seed until a weighting to subtract the weighting from is found
            i = whichweight
            while i == whichweight:
                seed += 1
                random.seed(seed)
                i = random.randrange(0, len(weightings))
            changingWeight2 = weightings[i] - howmuch
            seed += 1
        weightings[whichweight] = changingWeight1
        weightings[i] = changingWeight2

        #attempt to find a different route with the new adjusted weightings 
        route = findRoute(segments, nodes, whereRouting, weightings)
        isDifferent = True
        for firstRoute in routes:

            #similarity calculates what percentage of nodes the routes have in common
            similarity = len(set(route[whereRouting[1]][1:]).difference(set(firstRoute[1:])))/len(route[whereRouting[1]][1:]) * 100
            
            #if the two routes are not different enough the weights will be adjusted again
            if similarity < similarityNeeded:
                isDifferent = False
        if isDifferent:
            return route, seed

        escapeCounter += 1
    return None, seed






#find multiple routes for the user to choose between
def findMultipleRoutes(whereRouting,userID = 1, numberOfRoutes = 3):

    #get data from the database
    myDatabase = DatabaseMethods()
    segments = myDatabase.getAllEdges()
    nodes = myDatabase.getAllNodes()
    weightings = myDatabase.getUserWeights(userID)
    myDatabase.closeConnection()

    routes = []
    firstRoute = findRoute(segments, nodes, whereRouting, weightings)
    routes.append(firstRoute[whereRouting[1]]) # add first route to a list
    seed = int(whereRouting[0]+whereRouting[1]) # the seed is made to ensure that each time that the same 2 nodes are put in the same options are generated
    
    #find the correct number of different routes for the user to choose between
    while len(routes) < numberOfRoutes:
        newRoute, seed = findOtherRoutes(segments, nodes, whereRouting, routes, seed)
        if newRoute:
            routes.append(newRoute[whereRouting[1]])
    return routes