from operator import itemgetter
import random

import numpy
import scipy

from database_methods import DatabaseMethods


def findRoute(segments, nodes, whereRouting, weightings=None):
    #apply weightings to segments to create a single final weight for each segment
    weightedSegments = []
    if weightings:
        for segment in segments: #apply weightings to each segment
            segmentid, start, end, length = segment
            weight = length * weightings[0] *2
            weightingIterator = 1
            for node in nodes:
                if node[0] == start:
                    for tempWeight in node[1:]:
                        weight += float(tempWeight)*float(weightings[weightingIterator])*length
                        weightingIterator+=1
            weightingIterator = 1
            for node in nodes:
                if node[0] == end:
                    for tempWeight in node[1:]:
                        weight += float(tempWeight)*float(weightings[weightingIterator])*length
                        weightingIterator+=1
            weightedSegments.append((start, end, weight))
    else:
        for segment in segments: #if no weighting only length is used
            segid, start, end, length = segment
            weight = length
            weightedSegments.append((start, end, weight))

    distmatrixSize = int(nodes[-1][0])
    distMatrix = numpy.zeros((len(nodes), len(nodes)))
    
    for segment in weightedSegments:
        distMatrix[int(segment[0])][int(segment[1])] = segment[2]
        distMatrix[int(segment[1])][int(segment[0])] = segment[2]
    
    distances, pred = scipy.sparse.csgraph.dijkstra(distMatrix, return_predecessors=True)

    return distances, pred






def findOtherRoutes(segments, nodes, whereRouting, routes, weightings = [1, 0, 0, 0, 0], seed = 0, similarityNeeded = 20, removingNodes = False):
    escapeCounter = 0 #escape counter to set max iterations so does not loop forever

    # calculate the total of weightings so that when the weights are adjusted it adjusts them by an apropriate amount
    weightingsMagnitude = 0
    for weight in weightings:
        weightingsMagnitude += weight


    while escapeCounter < 10:

        #temp values for the weights that are changing to check a weight never goes below 0
        changingWeight1 = -1
        changingWeight2 = 1

        while changingWeight1 < 0 or changingWeight2 < 0:

            #calculate which weight is changing and by how much 
            random.seed(seed)
            whichweight = random.randrange(0, len(weightings))
            random.seed(seed)
            howmuch = random.uniform(0, weightingsMagnitude)
            changingWeight1 = weightings[whichweight] + howmuch

            #loop used to iterate seed until a weighting to subtract the weighting from is found
            i = whichweight
            while i == whichweight:
                seed += 1
                random.seed(seed)
                i = random.randrange(0, len(weightings))
            changingWeight2 = weightings[i] - howmuch
        weightings[whichweight] = changingWeight1
        weightings[i] = changingWeight2

        weightings = []
        for x in range(5):
            weightings.append(random.uniform(0, weightingsMagnitude))
            seed+=1

        if removingNodes == True:
            random.seed(seed)
            for singleRoute in routes:
                toRemove = random.choice(singleRoute)
                #print(nodes[3])
                #for x in range(len(nodes)):
                #    print(nodes[x][0])
                #    if nodes[x][0] == toRemove:
                #        nodes.pop(x)
                #        break
                #print(toRemove, "dhdd")
                exitready = False
                while exitready == False:
                    for x in range(len(segments)):
                            if segments[x][1] == toRemove:
                                segments.pop(x)
                                break
                            if segments[x][2] == toRemove:
                                segments.pop(x)
                                break
                    exitready = True
                        
                    



        #attempt to find a different route with the new adjusted weightings 
        routeweights, routePr = findRoute(segments, nodes, whereRouting, weightings)
        route = (getPath(routePr,whereRouting[0], whereRouting[1]))
        isDifferent = True
        for firstRoute in routes:
            #similarity calculates what percentage of nodes the routes have in common
            similarity = len(set(route).difference(set(firstRoute)))/len(route) * 100
            
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
    weightingstemp = myDatabase.getUserWeights(userID)
    weightingstemp = weightingstemp[0]
    myDatabase.closeConnection()

    print(weightingstemp)

    routes = []
    weightings = []

    largestWeight = 0
    for tempWeight in weightingstemp:
        if float(tempWeight) > largestWeight:
            largestWeight = float(tempWeight)
    for weightIterator in range(len(weightings)):
        weightings[weightIterator] = float(weightingstemp[weightIterator])/largestWeight
    firstRouteWeights, firstRoute = findRoute(segments, nodes, whereRouting, weightings)
    actualRoute = getPath(firstRoute, whereRouting[0], whereRouting[1])
    routes.append(actualRoute) # add first route to a list
    seed = int(whereRouting[0]+whereRouting[1]) # the seed is made to ensure that each time that the same 2 nodes are put in the same options are generated
    
    #find the correct number of different routes for the user to choose between
    iterator = 0
    while len(routes) < numberOfRoutes and iterator<3:
        newRoute, seed = findOtherRoutes(segments, nodes, whereRouting, routes, seed = seed)
        print(newRoute)
        if newRoute:
            print(newRoute)
            routes.append(newRoute)
        iterator += 1

    if len(routes) < numberOfRoutes:
        iterator = 0
        while len(routes) < numberOfRoutes and iterator<20:
            tempSegments = segments
            newRoute, seed = findOtherRoutes(tempSegments, nodes, whereRouting, routes, seed = seed, removingNodes = True)
            if newRoute:
                routes.append(newRoute)
            seed += 1
            iterator += 1


    print("AAAA", routes)
    while len(routes) < numberOfRoutes:
        routes.append(routes[0])
    return routes


def getPath(Pr,i,j):
    path = [int(j)]
    k = j
    while Pr[int(i)][int(k)]!= -9999:
        path.append(int(Pr[int(i)][int(k)]))
        k = Pr[int(i)][int(k)]
    return path[::-1]