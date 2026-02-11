import routefindingalgorithm

segments = [
    ("21289", "B", 5),
    ("B", "C", 2),
    ("21289", "C", 1),
    ("C", "D", 1),
    ("D", "1978476", 5),
    ("1978476", "F", 5),
    ("F", "G", 5),
    ("G", "C", 5),
    ("H", "F", 5),
    ("C", "J", 5),
    ("B", "D", 4),
    ("C", "1978476", 6),
    ("D", "F", 3)

]

nodes = {
    "21289" : (0, 0, 4, 3),
    "B": (5, 0, 5 , 4),
    "C": (9, 0, 3, 5),
    "D": (10,4 ,4, 4),
    "1978476": (15, 0, 4,8),
    "F": (20, 0,6,5),
    "G": (25, 0,4,3),
    "H": (30, 0,3,7),
    "I": (35, 0, 5,4),
    "J": (40, 0,4, 5)
}


whereRouting = ("21289", "1978476")


abba = routefindingalgorithm.findRoute(segments, nodes, whereRouting)
print(abba)
print(routefindingalgorithm.findOtherRoutes(segments, nodes, whereRouting, [abba[whereRouting[1]]]))
#print(routefindingalgorithm.findMultipleRoutes())