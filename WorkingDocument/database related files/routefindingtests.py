import routefindingalgorithm

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


abba = routefindingalgorithm.findRoute(segments, nodes, whereRouting)
print(abba)
print(routefindingalgorithm.findOtherRoutes(segments, nodes, whereRouting, [abba[whereRouting[1]]]))
#print(routefindingalgorithm.findMultipleRoutes())