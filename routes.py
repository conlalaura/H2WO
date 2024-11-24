from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

import models

# flask
main = Blueprint("main", __name__)

# mongodb
client = MongoClient(host="localhost", port=27017)
db = client["osm"]  # db
h2wo_collection = db["osm_h2wo"]  # project collection
h2wo_users = db["users"]  # users
# valid amenities for API
valid_amenities = ["all", "water", "toilets", "bench", "shelter", "waste_basket"]


@main.route("/")  # http://127.0.0.1:5000/
def root():
    """Render main page."""
    return render_template("page.html")


@main.route("/api", methods=["GET"])
def get_amenities():  # example: 127.0.0.1:5000/api?type=water
    amenity_type = request.args.get("type")  # access "type" parameter
    if amenity_type:
        if amenity_type not in valid_amenities:
            return (
                jsonify(
                    {
                        "error": f"Invalid type '{amenity_type}'. Valid types are: {', '.join(valid_amenities)}"
                    }
                ),
                400,
            )
    if amenity_type == "all":  # all project relevant amenities
        cursor = h2wo_collection.find()  # read amenities
        res = []  # store result in res
        for current_item in cursor:  # iterate over the cursor
            keys = current_item.keys()  # get all keys
            node_dict = {}  # fill res with required values
            for key in keys:
                if key != "_id":
                    node_dict[key] = current_item[key]
            res.append(node_dict)  # append dict to res
        return {"amenities": res}  # return as dictionary
    else:
        amenities = models.get_amenities(col=h2wo_collection, amenity_name=amenity_type)
        return jsonify(amenities)


@main.route("/registration", methods=["GET", "POST"])
def registration():
    """User registration"""
    if request.method == "POST":
        # Get data from website input
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Required registration information
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Check if user already exists
        if models.email_used(h2wo_users, email):
            flash("Email already registered! Please login!")
            return redirect(url_for("main.login"))
        else:
            # Create document for new user
            user = {
                "username": username,
                "password_hash": generate_password_hash(password),
                "email": email,
                "favourites": [],
            }
            models.insert_new_user(h2wo_users, user)
            flash(f"Welcome to H2WO {username}! You can now log in!")
            return redirect(url_for("main.login"))

    return render_template(
        "registration.html"
    )  # TODO: this is just a basic template. it does not look nice :(


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get data from website input
        email = request.form.get("email")
        password = request.form.get("password")

        # Required login information
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Verify user credentials
        user = models.get_user(h2wo_users, email)
        if user and user["password"] == password:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    return render_template(
        "login.html"
    )  # TODO: this is just a basic template. it does not look nice :(


@main.route("/chart")  # http://127.0.0.1:5000/statistics/
def chart():
    return render_template("chart.html")


@main.route("/map")
def h2wo_map():
    """render map page with amenities"""
    return render_template("map.html")
