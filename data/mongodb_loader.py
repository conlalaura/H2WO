import pymongo
import json

from werkzeug.security import generate_password_hash

import models

client = pymongo.MongoClient(host="localhost", port=27017)
db = client["osm"]  # select db
osm_collection = "osm_all_amenities"

"""
Create or load collection with all OpenSteetMap data
"""
# check if the collection already exists
if osm_collection in db.list_collection_names():
    print(f"Collection '{osm_collection}' has already been created.")
else:
    print(
        f"Collection '{osm_collection}' hasn't been created yet, will do that now for you :)."
    )

collection = db[osm_collection]  # load collection, will be created if not present

# load documents into collection if collection empty
if collection.count_documents({}) == 0:
    with open("data/osm-output.json", "r") as f:
        data = json.load(f)
        nodes = data["nodes"]
    # bulk insert
    result = collection.insert_many(nodes)
    print(f"Inserted {len(result.inserted_ids)} documents into '{osm_collection}'.")
else:
    print(
        f"The collection '{osm_collection}' already contains {collection.count_documents({})} documents. No data inserted."
    )

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
        results = collection.find(query, keys)
        filtered_amenities += (
            results  # append individual dicts/jsons to filtered_amenities
        )

    elif amenity == "water_point":
        # keys to keep
        keys = {"name": 1, "amenity": 1, "lat": 1, "lon": 1, "id": 1}
        query = {"amenity": amenity}
        results = collection.find(query, keys)
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
        results = collection.find(query, keys)
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
        results = collection.find(query, keys)
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
        results = collection.find(query, keys)
        filtered_amenities += (
            results  # append individual dicts/jsons to filtered_amenities
        )

    elif amenity == "water_tap":
        query = {"amenity": amenity}
        results = collection.find(query)
        filtered_amenities += (
            results  # append individual dicts/jsons to filtered_amenities
        )

    elif amenity == "waste_basket":
        # keys to keep
        keys = {"name": 1, "amenity": 1, "waste": 1, "lat": 1, "lon": 1, "id": 1}
        query = {"amenity": amenity}
        results = collection.find(query, keys)
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
        results = collection.find(query, keys)
        filtered_amenities += (
            results  # append individual dicts/jsons to filtered_amenities
        )

"""
Create or load new mongoDB collection with project-relevant data
"""
filtered_collection_name = "osm_h2wo"

# check if the collection already exists
if filtered_collection_name in db.list_collection_names():
    print(f"Collection '{filtered_collection_name}' has already been created.")
else:
    print(
        f"Collection '{filtered_collection_name}' hasn't been created yet, will do that now for you :)."
    )

h2wo_collection = db[
    filtered_collection_name
]  # load new collection, will be created if not present

# load documents into collection if collection empty
if h2wo_collection.count_documents({}) == 0:
    result = h2wo_collection.insert_many(filtered_amenities)
    print(
        f"Inserted {len(result.inserted_ids)} documents into '{filtered_collection_name}'."
    )
else:
    print(
        f"The collection '{filtered_collection_name}' already contains {h2wo_collection.count_documents({})} documents. No data inserted."
    )

"""
Create or load new mongoDB collection with users
"""
user_collection_name = "users"

# check if the collection already exists
if user_collection_name in db.list_collection_names():
    print(f"Collection '{user_collection_name}' has already been created.")
else:
    print(
        f"Collection '{user_collection_name}' hasn't been created yet, will do that now for you :)."
    )

users_collection = db[
    user_collection_name
]  # load new collection, will be created if not present

"""
Create a demo user
"""
# document for demo user
demo_user = {
    "username": "Demo-User",
    "password_hash": generate_password_hash("password"),
    "email": "demo@user.com",
    "favourites": [],
}

# create demo user if not present yet
if models.email_used(users_collection, demo_user["email"]):
    favourites = users_collection.find_one(
        {"email": "demo@user.com"}, {"favourites": 1, "_id": 0}
    )["favourites"]
    print(
        f"Demo User is already in the collection and has {len(favourites)} favourite places saved. :)"
    )
else:
    sample_size = 50
    models.insert_new_user(users_collection, demo_user)
    # select a few water-related documents to add to favourites. Use aggregation to match and sample
    query = {
        "amenity": {"$in": ["fountain", "water_point", "drinking_water", "water_tap"]}
    }

    pipeline = [
        {"$match": query},
        {"$sample": {"size": sample_size}},  # randomly sample 50 documents
        {"$project": {"_id": 1}},  # only use "_id" field
    ]

    random_documents = list(h2wo_collection.aggregate(pipeline))
    random_ids = [doc["_id"] for doc in random_documents]

    # add id's of random documents top the demo-users favourite
    users_collection.update_one(
        {"email": "demo@user.com"},  # find user by email
        {"$addToSet": {"favourites": {"$each": random_ids}}},  # add multiple ids,
    )
    print(
        f"Demo-User has been created and {sample_size} favourite places have been added!"
    )
