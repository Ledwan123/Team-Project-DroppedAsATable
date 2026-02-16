from database_methods import DatabaseMethods
import routefindingalgorithm

db = DatabaseMethods()
segments = [(seg[1], seg[2], seg[3]) for seg in db.getAllEdges()]
nodes = db.getAllNodes()

# Try a simple route
result = routefindingalgorithm.findRoute(segments, nodes, (1, 60))
print(f"Route to node 60: {result.get(60, 'Not found')}")

db.closeConnection()