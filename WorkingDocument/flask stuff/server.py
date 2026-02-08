from flask import render_template, Flask, request, redirect, jsonify
from database_methods import *
# from routefindingalgorithm import *
import json

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
        if request.is_json:
            data = request.get_json()
            print(data)
            print(data["username"])
            print(data["password"])
        else:
            print("false")
        
        return render_template("login.html")

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


@app.route("/missions_t1.html", methods=["GET"])
def missions_1r():
    return redirect('/missions1')

@app.route("/missions_t1", methods=["GET"])
def mission_1():
    return render_template("missions_t1.html")


@app.route("/missions_t2.html", methods=["GET"])
def missions_2r():
    return redirect('/missions1')

@app.route("/missions_t2", methods=["GET"])
def mission_2():
    return render_template("missions_t2.html")


@app.route("/missions_t3.html", methods=["GET"])
def missions_3r():
    return redirect('/missions3')

@app.route("/missions_t3", methods=["GET"])
def mission_3():
    return render_template("missions_t3.html")


@app.route("/user_profile.html", methods=["GET"])
def user_profiler():
    return redirect('/user_profile')

@app.route("/user_profile", methods=["GET"])
def user_profile():
    return render_template("user_profile.html")


if __name__ == "__main__":
    app.run()
    