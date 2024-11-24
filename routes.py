from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

import models

# flask
main = Blueprint("main", __name__)

# mongodb
client = MongoClient(host="localhost", port=27017)
db = client["osm"]  # db
osm_collection = db["osm_h2wo"]  # project collection
osm_users = db["users"]  # users


@main.route("/")  # http://127.0.0.1:5000/
def root():
    """Render main page."""
    return render_template("page.html")


@main.route("/api/osm_data")  # api for all project relevant data
def get_all_relevant_amenities():
    """Upload json of all project relevant amenities"""
    cursor = osm_collection.find()  # read amenities
    res = []  # store result in res
    for current_item in cursor:  # iterate over the cursor
        keys = current_item.keys()  # get all keys
        node_dict = {}  # fill res with required values
        for key in keys:
            if key != "_id":
                node_dict[key] = current_item[key]
        res.append(node_dict)  # append dict to res
    return {"amenities": res}  # return as dictionary


@main.route(
    "/api/water_data"
)  # api for water related amenities  #TODO change to one API with variable amenity: water, toilet etc.
def get_water_data():
    amenities = models.get_amenities(col=osm_collection, amenity_name="water")
    return jsonify(amenities)


@main.route("/api/toilet_data")  # api for toilets
def get_toilet_data():
    amenities = models.get_amenities(col=osm_collection, amenity_name="toilets")
    return jsonify(amenities)


@main.route("/api/bench_data")  # api for benches
def get_bench_data():
    amenities = models.get_amenities(col=osm_collection, amenity_name="bench")
    return jsonify(amenities)


@main.route("/api/shelter_data")  # api for shelter
def get_shelter_data():
    amenities = models.get_amenities(col=osm_collection, amenity_name="shelter")
    return jsonify(amenities)


@main.route("/api/waste_basket_data")  # api for waste baskets
def get_waste_basket_data():
    amenities = models.get_amenities(col=osm_collection, amenity_name="waste_basket")
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
        if models.email_used(osm_users, email):
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
            models.insert_new_user(osm_users, user)
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
        user = models.get_user(osm_users, email)
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
