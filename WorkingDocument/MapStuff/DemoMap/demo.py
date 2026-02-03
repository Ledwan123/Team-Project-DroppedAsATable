from flask import Flask, render_template, request, jsonify
import sqlite3
from database_methods import *

app = Flask(__name__)


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
    myDatabase.setup()

    node_id = data["id"]
    coordx = data["coordx"]
    coordy = data["coordy"]

    myDatabase.addNode(coordx, coordy)

    print(myDatabase.getMapData())

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
