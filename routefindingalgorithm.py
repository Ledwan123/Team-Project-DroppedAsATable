from operator import itemgetter
import random

segments = [
    ("A", "B", 5, 3, 6),
    ("B", "C", 2, 2, 5),
    ("A", "C", 1, 1, 8)
]

nodes = [
    ("A", 0, 0),
    ("B", 5, 0),
    ("C", 9, 0)
]


whereRouting = ("A", "C")

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
        whichweight = random.randrange(0, 2)
        howmuch = random.choice([-1, 1])
        weightings[whichweight] += howmuch
        route = findRoute(segments, nodes, whereRouting, [3, 2, 4])

        similarity = len(set(firstRoute) and set(route)) / float(len(set(firstRoute) or set(route))) * 100
        if similarity < 70:
            return route

        escapeCounter += 1
    return None



abba = findRoute(segments, nodes, whereRouting)
print(abba)
#print(findOtherRoutes(segments, nodes, whereRouting, abba))