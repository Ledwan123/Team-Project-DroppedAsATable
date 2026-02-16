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
    weights = data["weights"]

    
    # Get data from database
    myDatabase = DatabaseMethods()
    myDatabase.setUserWeights(1, weights)
    myDatabase.closeConnection()
    
    # Find route
    myDatabase = DatabaseMethods()
    all_results = routefindingalgorithm.findMultipleRoutes((start_node, end_node))
    print(all_results)
    coordinates = myDatabase.getPathCoordinates(all_results[0])
    coordinatesTwo = myDatabase.getPathCoordinates(all_results[1])
    coordinatesThree = myDatabase.getPathCoordinates(all_results[2])

    #calculate distance of each route
    costOne = 0
    for i in range(1, len(all_results[0][1:]) - 3):
        costOne += int(myDatabase.getEdgeLength(all_results[0][i], all_results[0][i + 1])[0][0])
    costTwo = 0
    for i in range(1, len(all_results[1][1:]) - 3):
        costTwo += int(myDatabase.getEdgeLength(all_results[1][i], all_results[1][i + 1])[0][0])
    costThree = 0
    for i in range(1, len(all_results[2][1:]) - 3):
        costThree += int(myDatabase.getEdgeLength(all_results[2][i], all_results[2][i + 1])[0][0])

    scoresOne = myDatabase.getScoreBreakdown(all_results[0][1:])
    scoresTwo = myDatabase.getScoreBreakdown(all_results[1][1:])
    scoresThree = myDatabase.getScoreBreakdown(all_results[2][1:])

    myDatabase.closeConnection()
    
    return jsonify({
        "success": True,
        "path": all_results[0],
        "pathTwo": all_results[1],
        "pathThree": all_results[2],
        "coordinates": coordinates,
        "coordinatesTwo": coordinatesTwo,
        "coordinatesThree": coordinatesThree,
        "costOne": costOne,
        "costTwo": costTwo,
        "costThree": costThree,
        "scoreOne": scoresOne,
        "scoreTwo": scoresTwo,
        "scoreThree": scoresThree,
        "start": start_node,
        "end": end_node
    })

@app.route("/getroutefromname", methods=["POST"])
def get_route_from_name():
    myDatabase = DatabaseMethods()
    data = request.get_json()
    start_name = data.get("startName", "")
    end_name = data.get("endName", "")

    
    start_node = myDatabase.getNodeFromLocation(start_name)
    end_node = myDatabase.getNodeFromLocation(end_name)
    print(start_node)
    raw_segments = myDatabase.getAllEdges()
    raw_nodes = myDatabase.getAllNodes()
    
    # Format segments for algorithm
    segments = [(seg[1], seg[2], seg[3]) for seg in raw_segments]
    nodes = raw_nodes  
    
    # Find route
    all_results = routefindingalgorithm.findMultipleRoutes((start_node, end_node))
    print(all_results)
    coordinates = myDatabase.getPathCoordinates(all_results[0])
    coordinatesTwo = myDatabase.getPathCoordinates(all_results[1])
    coordinatesThree = myDatabase.getPathCoordinates(all_results[2])
    myDatabase.closeConnection()
    
    return jsonify({
        "success": True,
        "path": all_results[0],
        "pathTwo": all_results[1],
        "pathThree": all_results[2],
        "coordinates": coordinates,
        "coordinatesTwo": coordinatesTwo,
        "coordinatesThree": coordinatesThree,
        "cost": 1,
        "costTwo": 2,
        "costThree": 3,
        "start": start_node,
        "end": end_node
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
    # Get the Codespace URL
    import os
    host = os.getenv('CODESPACE_NAME', '127.0.0.1')
    port = 5000
    
    print(f"🚀 Server starting...")
    print(f"📱 Access your app at: https://{host}-{port}.preview.app.github.dev")
    
    app.run(host='0.0.0.0', port=port, debug=True)
