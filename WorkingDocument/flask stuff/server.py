from flask import render_template, Flask, request, redirect, jsonify, make_response, url_for, session
from database_methods import *
# from routefindingalgorithm import *
import time

app = Flask(__name__)

DatabaseMethods

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
    elif request.method == "POST":
        if request.is_json:
            myDatabase = DatabaseMethods()
            try:
                data = request.get_json()

                # Checks if a username and password has actually been sent.
                if "username" not in data or "password" not in data:
                    myDatabase.closeConnection()
                    return "No username or password has been entered"

                # Checks if a non-blank username and password has actually been sent.
                if data["username"] == "" or data["password"] == "":
                    myDatabase.closeConnection()
                    return "No username or password has been entered"
                

                # Checks with the database to see if a user with this username exists.
                database_response = myDatabase.getLoginDetails(data["username"])

                # Checks if the response is blank.
                if database_response == None or database_response == []:
                    # Blanks response either means no user exists or bad database connection.
                    myDatabase.closeConnection()
                    return "Incorrect username or password has been entered"

                password = database_response[0][1]
                myDatabase.closeConnection()

                # If the passwords match then redirect the user to /map.
                if password == data["password"]:
                    return "/map"
                else:
                    return "Incorrect username or password has been entered"
            except:
                myDatabase.closeConnection()
                return "Incorrect username or password has been entered"
            
        else:
            return "Invalid request"

@app.route("/signup.html")
def signup_redirect():
    return redirect('signup')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Check with database
        return render_template("signup.html")
    

@app.route("/map.html")
def map_redirect():
    return redirect(url_for("map"))

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
    return redirect('/missions_t1')

@app.route("/missions_t1", methods=["GET"])
def mission_1():
    if request.method == "GET":
        myDatabase = DatabaseMethods()
        question1 = "Mission Description"
        id = 1
         
        try:
            database_response = myDatabase.getMissionQuestion(id)
            question1 = database_response[0][0]
        finally:
            myDatabase.closeConnection()
            return render_template("missions_t1.html", question1=question1)
    # elif request.method == "POST":
    #     data = request.get_json()
    #     print(data)
    #     # Get mission name and description from database using the mission id

    #     # Pass name and description through to the edit mission page



    #     print(url_for("edit_mission", id=data["number"]))
    #     return redirect(url_for("edit_mission", id=data["number"]))
    #     # return redirect(f"/edit_mission.html?id={data["number"]}")


@app.route("/missions_t2.html", methods=["GET"])
def missions_2r():
    return redirect('/missions_t2')

@app.route("/missions_t2", methods=["GET"])
def mission_2():
    return render_template("missions_t2.html")


@app.route("/missions_t3.html", methods=["GET"])
def missions_3r():
    return redirect('/missions_t3')

@app.route("/missions_t3", methods=["GET"])
def mission_3():
    return render_template("missions_t3.html")

@app.route("/edit_mission.html", methods=["GET"])
def edit_mission_r():
    return redirect("/edit_mission")

@app.route("/edit_mission", methods=["GET", "POST"])
def edit_mission():
    if request.method == "GET":
        myDatabase = DatabaseMethods()
        try:
            # Gets id from URL
            id = request.args.get('id', type=int)


            # Checks if ID variable is actually in the URL.
            if id == None:
                myDatabase.closeConnection()
                return redirect("/missions_t1")
            

            # Gets question from the URL.
            database_response = myDatabase.getMissionQuestion(id)

            print(database_response)
            if database_response == None or database_response == []:
                myDatabase.closeConnection()
                return redirect("/missions_t1")
            if database_response[0] == None:
                myDatabase.closeConnection()
                return redirect("/missions_t1")
            
            question = database_response[0][0]
            print(question)

            myDatabase.closeConnection()
            return render_template("edit_mission.html", question=question)
        except:
            myDatabase.closeConnection()
            return 500
    elif request.method == "POST":
        myDatabase = DatabaseMethods()

        try:

            try:
                data = request.get_json()
                id = data["id"]
                question = data["question"]
            except:
                id = None
                question = None

            print(f"ID: {id} \nQuestion: {question}")

            # Check to see if required arguments were sent
            if id == None or question == None:
                # Returns 400 BAD_REQUEST
                myDatabase.closeConnection()
                return 400
            
            print("Past the check")

            # [0][0] is startNode, [0][1] is endNode
            database_response = myDatabase.getMissionData(id)

            print(f"Response: {database_response}")

            # No mission with this ID exists
            if database_response == None or database_response == []:
                myDatabase.closeConnection()
                return 400


            # Change userID when implementing login system.
            # userID, missionID,newQuestion, newStartNode,newEndNode
            print("editing mission")
            myDatabase.editMission(1, id, question, database_response[0][0], database_response[0][1])
            myDatabase.closeConnection()
            print("About to redirect")
            return "/missions_t1"
        
        except:
            print("ERROR!")
            myDatabase.closeConnection()
            return 500
    
        

@app.route("/user_profile.html", methods=["GET"])
def user_profiler():
    return redirect('/user_profile')

@app.route("/user_profile", methods=["GET"])
def user_profile():
    return render_template("user_profile.html")

@app.route("/mission_display.html", methods=["GET"])
def mission_display_r():
    return redirect(url_for("mission_display"))

@app.route("/mission_display", methods=["GET", "POST"])
def mission_display():
    if request.method == "GET":
        myDatabase = DatabaseMethods()
        try:
            # Gets id from URL
            id = request.args.get('id', type=int)

            print("alone at the edge of the universe")

            # Checks if ID variable is actually in the URL.
            if id == None:
                myDatabase.closeConnection()
                return redirect(url_for("mission_1"))
            

            # Gets question from the URL.
            database_response = myDatabase.getMissionQuestion(id)

            if database_response == None or database_response == []:
                myDatabase.closeConnection()
                return redirect(url_for("mission_1"))
            if database_response[0] == None:
                myDatabase.closeConnection()
                return redirect(url_for("mission_1"))
            
            question = database_response[0][0]

            myDatabase.closeConnection()
            return render_template("mission_display.html", question=question)
        except:
            myDatabase.closeConnection()
            return redirect(url_for("mission_1"))
if __name__ == "__main__":
    app.run()
    