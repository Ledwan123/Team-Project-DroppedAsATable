from flask import render_template, Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login.html", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        # Check with database

@app.route("/signup.html", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Check with database


if __name__ == "__main__":
    app.run()
    