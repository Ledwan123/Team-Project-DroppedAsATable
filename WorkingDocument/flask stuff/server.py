from flask import render_template, Flask, request, redirect, jsonify
from database_methods import *
# from routefindingalgorithm import *

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('/login')

@app.route("/login.html")
def login_redirect():
    return redirect('login')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        # Check with database
        print("hello")
        pass

@app.route("/signup.html")
def signup_redirect():
    return redirect('signup')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Check with database
        pass

@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "GET":
        return render_template("map.html")
    if request.method == "POST":
        start = request.form["start"]
        end = request.form["end"]

        return "Route saved to database!"

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

@app.route("/route", methods=["POST"])
def calc_route():
    data = request.get_json()

    start_node = data["start"]
    end_node = data["end"]
    weights = data["weights"]

    route = findRoute(SEG, NODE, (start_node, end_node), weights)

    return route # ROUTE SHOULD BE GIVEN IN JSON FORMAT




if __name__ == "__main__":
    app.run()
    