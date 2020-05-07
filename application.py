import os
import numpy as np

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

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
db = SQL("sqlite:///skincare.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # GET method
    if request.method == "GET":
        return render_template("register.html")

    # POST method or others
    else:
        username = request.form.get("username") #request username
        password = request.form.get("password") #request password
        first_name = request.form.get("first_name") #request first name
        last_name = request.form.get("last_name") #request last name
        confirm_password = request.form.get("password confirmation") #request password confirmation

    #error messages
    if not request.form.get("username"):
        return apology("Please enter a username.")
    if not request.form.get("password"):
        return apology("Please enter a password.")
    if not request.form.get("password confirmation"):
        return apology("Please confirm password.")
    if password != confirm_password:
        return apology("Please make sure the two fields match.")

    # error messages
    if not request.form.get("username"):
        return apology("Please enter a username.")
    elif not request.form.get("password"):
        return apology("Please enter a password.")
    elif not request.form.get("password confirmation"):
        return apology("Please confirm password.")
    elif not request.form.get("first_name"):
            return apology("Please enter your first name.")
    elif not request.form.get("last_name"):
            return apology("Please enter your last name.")
    elif password != confirm_password:
        return apology("Please make sure the two fields match.")
    else:
        hash = generate_password_hash(password)
        new_user_id = db.execute("INSERT INTO users (username, hash, first_name, last_name) VALUES (:username, :hash, :first_name, :last_name)", username = username, hash = hash, first_name = first_name, last_name = last_name)
        flash("Registered!")
        return redirect("/login")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
def index():
    """Home page shows current favorites, empty if new user"""

    dictionary = db.execute("SELECT * FROM favorites WHERE user_id = :human_id", human_id = session["user_id"])
    return render_template("saved.html", dictionary=dictionary)


@app.route("/browse", methods=["GET", "POST"])
@login_required
def browse():
    """Search up by ingredients"""

    human_id = session["user_id"]

    #Create list of names by calling from database
    total_names = db.execute("SELECT DISTINCT name FROM products ORDER BY name ASC")
    name_list = []
    for row in total_names:
        name = row['name'].capitalize().strip()
        name_list.append(name)

    #GET method
    if request.method == "GET":
        return render_template("browse.html", name_list = name_list)

    #POST method or others
    else:
        if not request.form.get("symbol"):
            return apology("Enter a valid product name")
        name_selected = request.form.get("symbol").lower()
        info = db.execute("SELECT name, brand, ingredient_list, id FROM products WHERE name = :name_selected", name_selected = name_selected)

        #error message
        if not info:
            flash("Error! Product may not exist.")
            return render_template("browse.html", name_list = name_list)

        #call product reviews from reviews table to display on page
        reviews = db.execute("SELECT count(id) FROM favorites WHERE id = :prod_id", prod_id = info[0]['id'])
        testimonials = db.execute("SELECT testimonial, review_id FROM reviews WHERE productid = :prodid;", prodid = info[0]['id'])

        #convert ingredient_list, which was originally a text, to a list
        ingr = info[0]['ingredient_list']
        ingr_list = list(ingr.strip('[]').replace('\'','').split(','))

        #pass information to browsed.html
        return render_template("browsed.html", info = info, ingr_list = ingr_list, reviews = reviews, testimonials = testimonials)


@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    """Save products to favorites"""

    #GET method
    if request.method == "GET":
        return render_template("saved.html")

    #POST method or others:
    else:

        #access product id from save button on browsed.html page
        product_id = request.form["save_button"]
        info = db.execute("SELECT name, brand, ingredient_list, id FROM products WHERE id = :product_id", product_id = product_id)

        #check if product is already saved
        inFaves = db.execute("SELECT id, user_id FROM favorites WHERE user_id = :human_id AND id = :product_id", human_id = session["user_id"], product_id = product_id)
        if len(inFaves) == 0:
            db.execute("INSERT INTO favorites (user_id, name, ingredient, brand, id) VALUES (:user_id, :name, :ingredient, :brand, :product_id)", user_id = session["user_id"], name = info[0]['name'], ingredient = info[0]['ingredient_list'], brand = info[0]['brand'], product_id = info[0]['id'])
            flash("Saved!")
        else:
            flash("Already in favorites!")

        #call data from updated favorites table to pass to saved.html
        dictionary = db.execute("SELECT * FROM favorites WHERE user_id = :human_id", human_id = session["user_id"])
        return render_template("saved.html", dictionary=dictionary)


@app.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    """Show friends"""

    human_id = session["user_id"]
    people = db.execute("SELECT first_name, last_name, id FROM users WHERE NOT id = :human_id", human_id = session["user_id"])
    friends = db.execute("SELECT friend1id, friend2id FROM friends")

    isFriend = {}
    for friend in friends:
        if human_id == friend['friend1id']:
            isFriend[friend['friend2id']] = True
        elif human_id == friend['friend2id']:
            isFriend[friend['friend2id']] = True

    if request.method == "GET":
        if people == []:
            return render_template("friends.html", people = [], isFriend = isFriend)
        else:
            return render_template("friends.html", people = people, isFriend = isFriend)
    elif request.method == "POST":
        friend_id = request.form['add_friend']
        groupid = db.execute("INSERT INTO friends (friend1id, friend2id) Values(:friend1id, :friend2id);", friend1id = human_id, friend2id = int(friend_id))
    return redirect("/friends")

@app.route("/share", methods=["GET", "POST"])
@login_required
def share():
    """Share favorites with friends"""

    #call favorite products and friends for the user
    human_id = session["user_id"]
    data = db.execute("SELECT id, name, brand FROM favorites WHERE user_id = :human_id;", human_id = human_id)
    friend_data = db.execute("SELECT id, username, first_name FROM users WHERE id IN (SELECT friend1id FROM friends WHERE friend2id = :human_id GROUP BY friend2id);", human_id = human_id)
    friend_data2 = db.execute("SELECT id, username, first_name FROM users WHERE id IN (SELECT friend2id FROM friends WHERE friend1id = :human_id GROUP BY friend2id);", human_id = human_id)

    #initialize symbol_list (product name), friend_list (friend names), and fid_list (friend IDs)
    symbol_list = []
    friend_list = []
    fid_list = []

    #build symbol_list
    for row in data:
        ownid = row['id']
        ownname = row['name']
        symbol_list.append(ownname)

    #build friend_list and fid_list
    if not friend_data:
        friend_data = friend_data2
    for row in friend_data:
        fid = row['id']
        fname = row['username']
        ffname = row['first_name']
        friend_list.append(ffname)
        fid_list.append(fid)

    #GET method
    if request.method == "GET":
        return render_template("share.html", symbol_list = symbol_list, friend_list=friend_list, fid_list = fid_list)

    #POST method
    else:
        prod_get = request.form.get("Name")
        friend_get = request.form.get("Friend")
        product = db.execute("SELECT id, name, brand, ingredient_list FROM products WHERE name = :name", name = prod_get)
        if not db.execute("SELECT id FROM users WHERE first_name = :first_name", first_name = friend_get):
            return apology("Input the correct information")
        person_id = db.execute("SELECT id FROM users WHERE first_name = :first_name", first_name = friend_get)[0]["id"]

        if not prod_get:
            return apology("Select a valid product name")
        elif not friend_get:
            return apology("Select a valid friend")

        #insert product into favorites of the friend user is sharing with
        favorite_update = db.execute("INSERT INTO favorites (user_id, name, ingredient, brand, id, friend, friend_id) Values(:person_id, :name, :ingredient, :brand, :id, :bool, :friend_id);", person_id = person_id, name = product[0]['name'], ingredient = product[0]['ingredient_list'], brand = product[0]['brand'], id = product[0]['id'], bool = True, friend_id = human_id)
        flash("Shared!")
        return redirect("/")


@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    """Leave reviews for products saved to favorites"""

    #call data necessary
    human_id = session["user_id"]
    data = db.execute("SELECT id, name, brand FROM favorites WHERE user_id = :human_id;", human_id = human_id)

    #initalize list of product names
    symbol_list = []
    name = db.execute("SELECT username FROM users WHERE id = :user_id;", user_id = human_id)[0]['username']

    #build list of product names by iterating through data
    for row in data:
        ownname = row['name']
        symbol_list.append(ownname)

    #GET method
    if request.method == "GET":
        return render_template("review.html", symbol_list = symbol_list, name = name)

    #POST method or others
    else:
        #request values stored in the forms on review.html
        product_get = request.form.get("product")
        testimonial = request.form.get("prodreview")

        if not product_get:
            return apology("Enter a valid product name")
        elif not testimonial:
            return apology("Enter a valid review")

        #call product information
        product = db.execute("SELECT id, name, brand, ingredient_list FROM products WHERE name = :name", name = product_get)

        #insert review and product ID into reviews table
        review_update = db.execute("INSERT INTO reviews (testimonial, productid) VALUES(:testimonial, :prodid);", testimonial = testimonial, prodid = product[0]['id'] )
        flash("Reviewed!")

        #pass list of product names and name of user into review.html
        return render_template("review.html", symbol_list = symbol_list, name = name)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)