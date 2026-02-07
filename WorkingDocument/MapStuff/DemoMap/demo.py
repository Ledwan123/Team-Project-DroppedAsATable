from flask import Flask, render_template, request, jsonify
import sqlite3
from database_methods import *

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

    node_id = data["id"]
    coordx = data["coordx"]
    coordy = data["coordy"]
    lighting = data["lighting"]
    crime = data["crime"]
    greenery = data["greenery"]
    gradient = data["gradient"]
    myDatabase.addNode(coordx, coordy, lighting, crime, greenery, gradient)
    
    print(myDatabase.getMapData())
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
    myDatabase.addEdge(start_node, end_node, length)
    nodes, edges = myDatabase.getMapData()
    
    myDatabase.closeConnection()
    return jsonify({"status": "ok", "nodes": nodes, "edges": edges})
   

if __name__ == "__main__":
    myDatabase = DatabaseMethods()
    myDatabase.setup()
    myDatabase.closeConnection()
    app.run(debug=False)
