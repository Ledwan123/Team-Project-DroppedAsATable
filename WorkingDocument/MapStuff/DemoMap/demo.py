from flask import Flask, render_template, request, jsonify
import sqlite3
from database_methods import *
import routefindingalgorithm

app = Flask(__name__)
#lighting, greenery, elevation, crime, distance

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start = request.form["start"]
        end = request.form["end"]

        return "Route saved to database!"

    return render_template("index.html")
   
@app.route("/addnode", methods=["POST"])
def add_node():
    data = request.get_json()
    myDatabase = DatabaseMethods()

    node_id = data["nodeID"]
    coordx = data["coordinateX"]
    coordy = data["coordinateY"]
    lighting = data["lighting"]
    crime = data["crime"]
    greenery = data["greenery"]
    gradient = data["gradient"]
    print(node_id)
    if myDatabase.nodeExists(node_id):
        print("Exists")
        myDatabase.updateNode(node_id, coordx, coordy, lighting, crime, greenery, gradient)
        
    else:
        print("Does not exist")
        myDatabase.addNode(node_id, coordx, coordy, lighting, crime, greenery, gradient)
            
    nodes, edges = myDatabase.getMapData()
    
    myDatabase.closeConnection()
    return jsonify({"status": "ok", "nodes": nodes, "edges": edges})
    
@app.route("/addsegment", methods=["POST"])
def add_segment():
    data = request.get_json()
    myDatabase = DatabaseMethods()

    segment_id = data["id"]
    start_node = data["startNode"]
    end_node = data["endNode"]
    length = data["length"]
    ensure_node_exists(myDatabase, start_node)
    ensure_node_exists(myDatabase, end_node)
    myDatabase.addEdge(segment_id, start_node, end_node, length)
    nodes, edges = myDatabase.getMapData()
    
    myDatabase.closeConnection()
    return jsonify({"status": "ok", "nodes": nodes, "edges": edges})

@app.route("/editnode", methods=["POST"])
def edit_node():
    data = request.get_json()
    myDatabase = DatabaseMethods()

    start_node = data["id"]
    myDatabase.deleteEdgeByStartNode(start_node)
    nodes, edges = myDatabase.getMapData()
    myDatabase.closeConnection()
    return jsonify({"status":"ok", "nodes":nodes, "edges":edges})
    
@app.route("/getroute", methods=["POST"])
def get_route():
    data = request.get_json()
    start_node = int(data["startNode"])
    end_node = int(data["endNode"])
    
    # Get data from database
    myDatabase = DatabaseMethods()
    raw_segments = myDatabase.getAllEdges()
    raw_nodes = myDatabase.getAllNodes()
    
    # Format segments for algorithm
    segments = [(seg[1], seg[2], seg[3]) for seg in raw_segments]
    nodes = raw_nodes  
    
    # Find route
    all_results = routefindingalgorithm.findRoute(segments, nodes, (start_node, end_node))
    
    if end_node in all_results:
        # Extract just the node path
        route_path = all_results[end_node][1:]
        
        # Get coordinates for the path
        coordinates = myDatabase.getPathCoordinates(route_path)
        
        myDatabase.closeConnection()
        
        return jsonify({
            "success": True,
            "path": route_path,
            "coordinates": coordinates,
            "cost": all_results[end_node][0],
            "start": start_node,
            "end": end_node
        })
    else:
        myDatabase.closeConnection()
        return jsonify({
            "success": False,
            "message": "No route found"
        })

@app.route("/getmapdata", methods=["GET"])
def mapdata():
    myDatabase = DatabaseMethods()
    nodes, edges = myDatabase.getMapData()
    myDatabase.closeConnection()
    return jsonify({"nodes": nodes, "edges": edges})

def ensure_node_exists(database, node_id):
    if not database.nodeExists(node_id):
        database.addPlaceholderNode(node_id)
   

if __name__ == "__main__":
    # Create a separate function to test the database
    def test_database():
        myDatabase = DatabaseMethods()
        nodes, edges = myDatabase.getMapData()
        myDatabase.closeConnection()
    
    # Call the test function
    myDatabase = DatabaseMethods()
    myDatabase.setup()
    myDatabase.closeConnection()
    
    # Test the database
    test_database()
    
    # Get the Codespace URL
    import os
    host = os.getenv('CODESPACE_NAME', '127.0.0.1')
    port = 5000
    
    print(f"🚀 Server starting...")
    print(f"📱 Access your app at: https://{host}-{port}.preview.app.github.dev")
    
    app.run(host='0.0.0.0', port=port, debug=True)
