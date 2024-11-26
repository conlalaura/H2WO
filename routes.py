from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

import models
from lib.Review import Review

# flask
main = Blueprint("main", __name__)

# mongodb
client = MongoClient(host="localhost", port=27017)
db = client["osm"]  # db
h2wo_collection = db["osm_h2wo"]  # project collection
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
        amenities = models.get_amenities(
            amenity_col=h2wo_collection, amenity_name=amenity_type
        )
        return jsonify(amenities)


@main.route("/chart")  # http://127.0.0.1:5000/statistics/
def chart():
    return render_template("chart.html")


@main.route("/map")
def h2wo_map():
    """render map page with amenities"""
    return render_template("map.html")


@main.route("/review/<int:amenity_id>", methods=["GET", "POST"])
def review(amenity_id):
    if request.method == "POST":
        review_username = request.form["Username"]
        review_rating = int(request.form["rating"])
        review_comment = request.form["comment"]
        # create review
        input_review = Review(username=review_username, rating=review_rating, comment=review_comment)
        # load into mongodb
        models.insert_review(amenity_col=h2wo_collection, amenity_id=amenity_id, review=input_review)
        # redirect to thank you page
        return redirect(url_for('thank_you'))
    return render_template("review.html")


@main.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")
