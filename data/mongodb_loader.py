from pymongo.collection import Collection
from werkzeug.security import generate_password_hash
import pymongo
import models
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = pymongo.MongoClient(host="localhost", port=27017)
db = client["osm"]  # select db
osm_collection_name = "osm_all_amenities"


def check_or_create_collection(
    collection_name: str, database: pymongo.database.Database
) -> Collection:
    # check if the collection already exists
    if collection_name in database.list_collection_names():
        print(f"Collection '{collection_name}' has already been created.")
    else:
        print(
            f"Collection '{collection_name}' hasn't been created yet, will do that now for you :)."
        )
    return db[collection_name]  # load collection, will be created if not present


def insert_if_empty(col: Collection, documents) -> None:
    if col.count_documents({}) == 0:
        # bulk insert
        col.insert_many(documents)
        print(f"Inserted {len(documents)} documents into '{col.name}'.")
    else:
        print(
            f"The collection '{col.name}' already contains {col.count_documents({})} documents. No data inserted."
        )


if __name__ == "__main__":

    """
    Create or load collection with all OpenSteetMap data
    """
    osm_collection = check_or_create_collection(
        collection_name=osm_collection_name, database=db
    )

    with open("data/osm-output.json", "r") as f:
        data = json.load(f)
        nodes = data["nodes"]

    # load documents into collection if collection empty
    insert_if_empty(col=osm_collection, documents=nodes)

    """
    Select only project-relevant data from the OpenSteetMap 
    """
    # relevant amenities for h2wo project
    amenities = [
        # always keep tags  lat, lon, name, amenity and id
        "fountain",  # special tags: drinking_water=yes/no
        "water_point",  # info: water form this amenity is defined as drinking water
        "drinking_water",  # special tags: wheelchair, bottle, seasonal
        "toilets",  # special tags: fee, wheelchair, changing_table, male, female, unisex
        "bench",  # special tags: seats, covered
        "water_tap",  # no special tags used
        "waste_basket",  # special tags: waste (separated by ;)
        "shelter",  # special tags: bench, bin, picnic_table, table, drinking_water
    ]

    # will be filled with relevant amenities
    filtered_amenities = []

    for amenity in amenities:
        if amenity == "fountain":
            # keys to keep
            keys = {
                "name": 1,
                "amenity": 1,
                "drinking_water": 1,
                "lat": 1,
                "lon": 1,
                "id": 1,
            }
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "water_point":
            # keys to keep
            keys = {"name": 1, "amenity": 1, "lat": 1, "lon": 1, "id": 1}
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "drinking_water":
            # keys to keep
            keys = {
                "name": 1,
                "amenity": 1,
                "wheelchair": 1,
                "bottle": 1,
                "seasonal": 1,
                "lat": 1,
                "lon": 1,
                "id": 1,
            }
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "toilets":
            # keys to keep
            keys = {
                "name": 1,
                "amenity": 1,
                "fee": 1,
                "wheelchair": 1,
                "changing_table": 1,
                "male": 1,
                "female": 1,
                "unisex": 1,
                "lat": 1,
                "lon": 1,
                "id": 1,
            }
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "bench":
            # keys to keep
            keys = {
                "name": 1,
                "amenity": 1,
                "seats": 1,
                "covered": 1,
                "lat": 1,
                "lon": 1,
                "id": 1,
            }
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "water_tap":
            query = {"amenity": amenity}
            results = osm_collection.find(query)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "waste_basket":
            # keys to keep
            keys = {"name": 1, "amenity": 1, "waste": 1, "lat": 1, "lon": 1, "id": 1}
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

        elif amenity == "shelter":
            # keys to keep
            keys = {
                "name": 1,
                "amenity": 1,
                "bench": 1,
                "bin": 1,
                "picnic_table": 1,
                "table": 1,
                "drinking_water": 1,
                "fee": 1,
                "lat": 1,
                "lon": 1,
                "id": 1,
            }
            query = {"amenity": amenity}
            results = osm_collection.find(query, keys)
            filtered_amenities += (
                results  # append individual dicts/jsons to filtered_amenities
            )

    """
    Create or load new mongoDB collection with project-relevant data
    """
    filtered_collection_name = "osm_h2wo"
    h2wo_collection = check_or_create_collection(
        collection_name=filtered_collection_name, database=db
    )
    # load documents into collection if collection empty
    insert_if_empty(col=h2wo_collection, documents=filtered_amenities)

    """
    Create or load new mongoDB collection with review
    """
    review_collection_name = "reviews"

    """
    Create or load new mongoDB collection with users
    """
    # user_collection_name = "users"
    # users_collection = check_or_create_collection(
    #     collection_name=user_collection_name, database=db
    # )
    """
    Create a demo user
    """
    # # document for demo user
    # demo_user = {
    #     "username": "Demo-User",
    #     "password_hash": generate_password_hash("password"),
    #     "email": "demo@user.com",
    #     "favourites": [],
    # }
    # #
    # # create demo user if not present yet
    # if models.email_used(users_collection, demo_user["email"]):
    #     favourites = users_collection.find_one(
    #         {"email": "demo@user.com"}, {"favourites": 1, "_id": 0}
    #     )["favourites"]
    #     print(
    #         f"Demo User is already in the collection and has {len(favourites)} favourite places saved. :)"
    #     )
    # else:
    #     sample_size = 50
    #     models.insert_new_user(users_collection, demo_user)
    #     # select a few water-related documents to add to favourites. Use aggregation to match and sample
    #     query = {
    #         "amenity": {"$in": ["fountain", "water_point", "drinking_water", "water_tap"]}
    #     }
    #
    #     pipeline = [
    #         {"$match": query},
    #         {"$sample": {"size": sample_size}},  # randomly sample 50 documents
    #         {"$project": {"_id": 1}},  # only use "_id" field
    #     ]
    #
    #     random_documents = list(h2wo_collection.aggregate(pipeline))
    #     random_ids = [doc["_id"] for doc in random_documents]
    #
    #     # add id's of random documents top the demo-users favourite
    #     users_collection.update_one(
    #         {"email": "demo@user.com"},  # find user by email
    #         {"$addToSet": {"favourites": {"$each": random_ids}}},  # add multiple ids,
    #     )
    #     print(
    #         f"Demo-User has been created and {sample_size} favourite places have been added!"
    #     )
