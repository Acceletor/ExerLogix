import requests
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json
from datetime import datetime

from helper import login_required, apology

# Configure application
app = Flask(__name__)

# Nutritionix API
API_ID = "eb2155c2"
API_KEY ="37bd4145ea0c3aef361a0a4b818f4e64"


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///exercise_log.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET","POST"])
@login_required
def index():
    """Show dashboard"""
    current_weight = db.execute("SELECT weight FROM weightlogs WHERE user_id = :user_id ORDER BY timestamp DESC LIMIT 1", user_id =session["user_id"])
    username = db.execute("SELECT username FROM users WHERE id= :user_id", user_id=session["user_id"])[0]

    list= db.execute("SELECT weight, date(timestamp) as date FROM weightlogs WHERE user_id = :user_id ORDER BY timestamp", user_id =session["user_id"])
    weightList = [n["weight"] for n in list]
    dateList = [n["date"] for n in list]
    goalweight= db.execute("SELECT goalweight FROM userdetails WHERE user_id= :user_id",user_id =session["user_id"])

    today_date= datetime.now().strftime("%d/%m/%Y")

    today_calories_burn = db.execute("SELECT SUM(calories) as todayCalSum FROM exerciselogs WHERE user_id= :user_id AND DATE(timestamp)= DATE('now');",
                                     user_id=session["user_id"])

    cal_list = db.execute("SELECT DATE(timestamp) as date,SUM(calories) as todayCalSum FROM exerciselogs  WHERE user_id = :user_id GROUP BY DATE(timestamp);",
                           user_id= session["user_id"])
    calorieslist= [n["date"] for n in cal_list]
    dateList_cal= [n["todayCalSum"] for n in cal_list]
    print(calorieslist)
    print(dateList_cal)

    return render_template("index.html", username=username, current_weight= current_weight, weightList=json.dumps(weightList), dateList=json.dumps(dateList),
                           goalweight=goalweight, today_date=today_date, today_calories_burn=today_calories_burn, calorieslist=json.dumps(calorieslist), dateList_cal=json.dumps(dateList_cal) )

@app.route("/login", methods=["GET","POST"])
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/register", methods=["GET","POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirm_ps = request.form.get("confirmation")

        if not name or not password or not confirm_ps:
            return apology("must fill all the form", 400)
        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE username= ?", name)

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("Username already exists", 400)
        # verified the confirm password and password
        if password == confirm_ps:
            hash = generate_password_hash(password)
            # save username and hashed password in database
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", name, hash)

            # remember the user while login
            rows = db.execute("SELECT * FROM users WHERE username = ?", name)
            session["user_id"] = rows[0]["id"]

        else:
            return apology("passwords do not match")

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/weight", methods=["GET","POST"])
@login_required
def weight():
    username = db.execute(
        "SELECT username FROM users WHERE id= :user_id", user_id=session["user_id"]
    )[0]

    if request.method == "POST":

        weight = request.form.get("weight")

        if not weight or not weight.isdigit() or int(weight) <= 0:
            return redirect("/weight")
        db.execute("INSERT INTO weightlogs (user_id, weight) VALUES (:user_id, :weight)",
            user_id=session["user_id"],
            weight=weight,
        )
        return redirect("/weight")

    weights = db.execute(
           "SELECT id, weight, date(timestamp) as date FROM weightlogs WHERE user_id= :user_id ORDER BY timestamp DESC",
           user_id=session["user_id"]
    )

    return render_template("weight.html",username=username, weights=weights)

@app.route("/delete_weight/<int:id>")
@login_required
def delete_weight(id):
    db.execute("DELETE FROM weightlogs WHERE id = :id",id=id)
    return redirect("/weight")

@app.route("/exercise", methods=["GET","POST"])
@login_required
def exercise():
    username = db.execute(
        "SELECT username FROM users WHERE id= :user_id", user_id=session["user_id"]
    )[0]

    current_weight= db.execute("SELECT weight FROM weightlogs WHERE user_id = :user_id ORDER BY timestamp DESC LIMIT 1", user_id =session["user_id"])

    check_profile= db.execute("SELECT * FROM userdetails WHERE user_id=:user_id", user_id=session["user_id"])

    if request.method == "POST":

        if not current_weight and not check_profile:
            return redirect("/exercise")

        workout_text=request.form.get("text")

        if not workout_text:
            return redirect("/exercise")

        GENDER = check_profile[0]["gender"]
        WEIGHT_KG = current_weight[0]["weight"]
        HEIGHT = check_profile[0]["height"]
        AGE = check_profile[0]["age"]

        header= {
            "x-app-id": API_ID,
            "x-app-key": API_KEY,
        }

        exercise_params = {
            "query":workout_text,
            "gender": GENDER,
            "weight_kg":WEIGHT_KG,
            "height_cm":HEIGHT,
            "age":AGE
        }

        exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


        response = requests.post(url=exercise_endpoint, json=exercise_params, headers=header)
        response.raise_for_status()
        result = response.json()

        print(result)

        for n in result["exercises"]:
            db.execute("INSERT INTO exerciselogs (user_id, exercise, calories, duration, met) VALUES (:user_id, :exercise , :calories, :duration, :met)",
                       user_id=session["user_id"],
                        exercise= n["user_input"],
                        duration= n["duration_min"],
                        met= n["met"],
                        calories= n["nf_calories"]
            )

        return redirect("/exercise")


    exercises_list= db.execute("SELECT *, date(timestamp) as date FROM exerciselogs WHERE user_id= :user_id ORDER BY timestamp DESC", user_id=session["user_id"])

    return render_template("exercise.html",username=username, check_profile=check_profile, current_weight=current_weight, exercises_list=exercises_list)

@app.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    username = db.execute(
        "SELECT username FROM users WHERE id= :user_id", user_id=session["user_id"]
    )[0]

    if request.method == "POST":
        gender = request.form.get("gender").lower()
        height = request.form.get("height")
        age = request.form.get("age")
        goalweight = request.form.get("goalweight")

        if gender not in ["female","male"] or not height or int(height) <= 0 or not age or int(age) <= 0 or not goalweight or int(goalweight) <= 0:
            return redirect("/profile")

        lists = db.execute("SELECT * FROM userdetails WHERE user_id= :user_id", user_id=session["user_id"])

        if not lists:
            db.execute("INSERT INTO userdetails (user_id, gender, height, age, goalweight) VALUES (:user_id, :gender, :height, :age, :goalweight)",
                        user_id=session["user_id"], gender=gender, height=height, age=age, goalweight=goalweight)
        else:
            db.execute("UPDATE userdetails SET gender= :gender, height= :height, age= :age, goalweight= :goalweight WHERE user_id = :user_id",
                         user_id=session["user_id"], gender=gender, height=height, age=age, goalweight=goalweight)

        return redirect("/profile")

    current_weight= db.execute("SELECT weight FROM weightlogs WHERE user_id = :user_id ORDER BY timestamp DESC LIMIT 1", user_id =session["user_id"])

    profilelist = db.execute("SELECT * FROM userdetails WHERE user_id=:user_id", user_id=session["user_id"])

    return render_template("profile.html",username=username, profilelist=profilelist, current_weight=current_weight)

@app.route("/delete_exercise/<int:id>")
@login_required
def delete_exercise(id):
    db.execute("DELETE FROM exerciselogs WHERE id = :id",id=id)
    return redirect("/exercise")