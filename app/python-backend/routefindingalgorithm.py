from operator import itemgetter
import random

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
            weight = length
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


def findOtherRoutes(segments, nodes, whereRouting, firstRoute, weightings = [1, 0, 0]):
    escapeCounter = 0
    while escapeCounter < 1000:
        whichweight = random.randrange(0, 3)
        howmuch = random.choice([-1, 1])
        weightings[whichweight] += howmuch
        route = findRoute(segments, nodes, whereRouting, weightings)
        similarity = len(set(route[whereRouting[1]][1:]).difference(set(firstRoute[whereRouting[1]][1:])))/len(route[whereRouting[1]][1:]) * 100
        if similarity > 0:
            return route

        escapeCounter += 1
    return None



abba = findRoute(segments, nodes, whereRouting)
print(abba)
print(findOtherRoutes(segments, nodes, whereRouting, abba))