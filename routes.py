from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

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
    # collect basic statistics for homepage
    count_data = models.get_homepage_data(osm_col=h2wo_collection)
    data_dict = {item["_id"]: item["count"] for item in count_data}
    # pass data_dict as data to access from home.html
    return render_template("home.html", data=data_dict)


@main.route("/api/amenities/<amenity_type>", methods=["GET"])
def get_amenities(amenity_type):  # example: 127.0.0.1:5000/api?type=water
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
            osm_col=h2wo_collection, amenity_name=amenity_type
        )
        return jsonify(amenities)


@main.route("/api/toilet_statistics_data", methods=["GET"])
def toilet_statistics_data():
    result = models.get_toilet_statistics_data(amenity_col=h2wo_collection)
    return jsonify(result)


@main.route("/api/sparsity_statistics_data", methods=["GET"])
def sparsity_statistics_data():
    result = models.get_sparsity_statistics_data(amenity_col=h2wo_collection)
    return jsonify(result)


@main.route("/statistics")
def statistics():
    return render_template("statistics.html")


@main.route("/map")
def h2wo_map():
    """render map page with amenities"""
    return render_template("map.html")


@main.route("/api/review/<amenity_id>", methods=["GET", "POST"])
def review(amenity_id):
    if request.method == "POST":
        # Parse the JSON data from the request body
        data = request.get_json()
        review_username = data.get("username")
        review_rating = int(data.get("rating"))
        review_comment = data.get("comment")
        # create review
        input_review = Review(
            username=review_username, rating=review_rating, comment=review_comment
        )
        # load into mongodb
        models.insert_review(
            amenity_col=h2wo_collection, amenity_id=amenity_id, review=input_review
        )
        return jsonify(data)
    if request.method == "GET":
        res = models.get_reviews(
            amenity_col=h2wo_collection, amenity_id=str(amenity_id)
        )
        return jsonify(res)


@main.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")
