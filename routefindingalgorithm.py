import random

segments = {
    "1": ("A", "B", 5, 3, 6),
    "2": ("B", "C", 4, 2, 5),
    "3": ("A", "C", 11, 1, 8)
}

nodes = {
    "1": ("A", 0, 0),
    "2": ("B", 5, 0),
    "3": ("C", 9, 0)
}


whereRouting = ("A", "C")

def findRoute(segments, nodes, whereRouting, weightings=None):
    distances = {}
    for a in nodes.values():
        distances[a[0]] = [float('inf'), whereRouting[0]]
    distances[whereRouting[0]] = [0, whereRouting[0]]
    
    for a in segments.values():
        start, end, length, light, traffic_level = a
        if weightings:
            weight = (length * weightings[0] + light * weightings[1] + traffic_level * weightings[2])
        else:
            weight = length

        for b in distances.items():
            if b[-1][-1] == start: 
                if distances[end][0] > b[-1][0] + weight:
                    distances[end] = ([b[-1][0] + weight] + b[-1][1:] + [end])
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
            foundRoute = True
            return route

        escapeCounter += 1
    return None



abba = findRoute(segments, nodes, whereRouting)
print(abba)
print(findOtherRoutes(segments, nodes, whereRouting, abba))