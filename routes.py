from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient

# flask
main = Blueprint("main", __name__)

# mongodb
client = MongoClient(host="localhost", port=27017)
db = client["osm"]  # select db
collection = db["osm_h2wo"]  # select collection


@main.route("/")  # http://127.0.0.1:5000/
def root():
    """Render the main page."""
    return render_template("page.html")


@main.route("/statistics/")  # http://127.0.0.1:5000/chart/
def statistics():
    return render_template("chart.html")


@main.route("/api/osm_data")  # http://127.0.0.1:5000/api/osm_data
def get_all_relevant_amenities():
    cursor = collection.find()  # read amenities
    res = []  # store result in res
    for current_item in cursor:  # iterate over the cursor
        keys = current_item.keys()  # get all keys
        node_dict = {}  # fill res with required values
        for key in keys:
            if key != "_id":
                node_dict[key] = current_item[key]
        res.append(node_dict)  # append dict to res
    return {"amenities": res}  # return as dictionary
