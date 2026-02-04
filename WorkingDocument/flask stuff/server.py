from flask import render_template, Flask, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('/login')

@app.route("login.html")
def login_redirect():
    return redirect('login')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        # Check with database
        pass

@app.route("signup.html")
def signup_redirect():
    return redirect('signup')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        # Check with database
        pass


if __name__ == "__main__":
    app.run()
    