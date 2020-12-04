import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required # lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///crm.db")

#Define Cohorts
COHORTS = [

    "Blue",
    "Red",
    "Silver",
    "Green",
    "Gold",
    "Orange",
    "Purple"
]

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    """Register user"""
    if request.method == "POST":

        # create variables for future reference
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check that user has completed all fields
        if not username or not password or not confirmation:
            return apology("Please complete all fields")

        # checks if username is taken and returns error message
        users = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(users) == 1:
            return apology("Username taken")

        # ensures matching passwords
        if not password == confirmation:
            return apology("Passwords must match")

        else:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            session["user_id"]=db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
            return redirect("/")

    return render_template("create_account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/")
@login_required
def SOM_network():
    network = db.execute("SELECT * FROM network")
    return render_template("SOM_network.html", network = network)


@app.route("/add_info", methods=["GET", "POST"])
@login_required
def add_info():

    if request.method == "POST":
        name = request.form.get("name")
        cohort = request.form.get("cohort")
        hometown = request.form.get("hometown")
        past_industry = request.form.get("past_industry")
        goal_industry = request.form.get("goal_industry")
        print(name)
        db.execute("INSERT INTO network (name, cohort, hometown, past_industry, goal_industry) VALUES (?, ?, ?, ?, ?)", name, cohort, hometown, past_industry, goal_industry)
        return redirect("/")

    else:
        return render_template("add_info.html", cohorts = COHORTS)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
     return render_template("quiz.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
