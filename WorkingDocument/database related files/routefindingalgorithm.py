from operator import itemgetter
import random

from database_methods import DatabaseMethods

segments = [
    ("A", "B", 5, 3, 6),
    ("B", "C", 2, 2, 5),
    ("A", "C", 1, 1, 8),
    ("C", "D", 1, 5, 2),
    ("D", "E", 5, 2, 4),
    ("E", "F", 5, 3, 6),
    ("F", "G", 5, 4, 7),
    ("G", "C", 5, 2, 3),
    ("H", "F", 5, 1, 5),
    ("C", "J", 5, 3, 6),
    ("B", "D", 4, 4, 4),
    ("C", "E", 6, 2, 5),
    ("D", "F", 3, 3, 7)

]

nodes = [
    ("A", 0, 0),
    ("B", 5, 0),
    ("C", 9, 0),
    ("D", 10, 0),
    ("E", 15, 0),
    ("F", 20, 0),
    ("G", 25, 0),
    ("H", 30, 0),
    ("I", 35, 0),
    ("J", 40, 0)
]


whereRouting = ("A", "J")

def findRoute(segments, nodes, whereRouting, weightings=None):

    #apply weightings to segments to create a single final weight for each segment
    weightedSegments = []
    if weightings:
        for a in segments: #apply weightings to each segment
            start, end, length, light, traffic_level = a
            weight = (length * weightings[0] + light * weightings[1] + traffic_level * weightings[2])
            weightedSegments.append((start, end, weight))
    else:
        for a in segments: #if no weighting only length is used
            start, end, length, light, traffic_level = a
            weight = length*1000
            weightedSegments.append((start, end, weight))

    #sort segments by weight to make priority queue
    sortedSegments = sorted(weightedSegments, key=itemgetter(2)) #sort by segment weight

    #initialize distances dictionary
    distances = {}
    for a in nodes:
        distances[a[0]] = [float('inf')] #distances will start as infinite
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


def findOtherRoutes(segments, nodes, whereRouting, routes, weightings = [1000, 0, 0], seed = 0):
    escapeCounter = 0 #escape counter to set max iterations so does not loop forever

    while escapeCounter < 1000:

        #temp values for the weights that are changing to check a weight never goes below 0
        x = -1
        y = -1

        while x < 0 or y < 0:

            #calculate which weight is changing and by how much 
            random.seed(seed)
            whichweight = random.randrange(0, len(weightings))
            random.seed(seed)
            howmuch = random.randrange(0, 100)
            x = weightings[whichweight] + howmuch

            #loop used to iterate seed until a weighting to subtract the weighting from is found
            i = whichweight
            while i == whichweight:
                seed += 1
                random.seed(seed)
                i = random.randrange(0, len(weightings))
            y = weightings[i] - howmuch
            seed += 1
        weightings[whichweight] = x
        weightings[i] = y

        #attempt to find a different route with the new adjusted weightings 
        route = findRoute(segments, nodes, whereRouting, weightings)
        isDifferent = True
        for firstRoute in routes:

            #similarity calculates what percentage of nodes the routes have in common
            similarity = len(set(route[whereRouting[1]][1:]).difference(set(firstRoute[1:])))/len(route[whereRouting[1]][1:]) * 100
            
            #if the two routes are not different enough the weights will be adjusted again
            if similarity < 10:
                isDifferent = False
        if isDifferent:
            return route, seed

        escapeCounter += 1
    return None, seed



#find multiple routes for the user to choose between
def findMultipleRoutes():
    #user will select between three routes
    numberOfRoutes = 3

    #which user is playing
    userID = 1

    #get data from the database
    segments = DatabaseMethods.getAllEdges(userID)
    nodes = DatabaseMethods.getAllNodes()
    weightings = DatabaseMethods.getUserWeights()

    #get which nodes the route is between
    whereRouting = () 

    routes = []
    firstRoute = findRoute(segments, nodes, whereRouting, weightings)
    routes.append(firstRoute[whereRouting[1]]) # add first route to a list
    seed = int(whereRouting[0]+whereRouting[1])
    
    #find the correct number of different routes for the user to choose between
    while len(routes) < numberOfRoutes:
        newRoute, seed = findOtherRoutes(segments, nodes, whereRouting, routes, seed)
        if newRoute:
            routes.append(newRoute[whereRouting[1]])
    return routes





abba = findRoute(segments, nodes, whereRouting)
print(abba)
print(findOtherRoutes(segments, nodes, whereRouting, [abba[whereRouting[1]]]))
#print(findMultipleRoutes())