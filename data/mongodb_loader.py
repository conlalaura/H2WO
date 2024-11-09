import pymongo
import json

client = pymongo.MongoClient(host="localhost", port=27017)
db = client["osm"]  # select db
collection_name = "osm"

"""
Create (or load) collection with all OpenSteetMap data
"""
# check if the collection already exists
if collection_name in db.list_collection_names():
    print(f"Collection '{collection_name}' has already been created.")
else:
    print(
        f"Collection '{collection_name}' hasn't been created yet, will do that now for you :)."
    )

collection = db[collection_name]  # load collection, will be created if not present

# load documents into collection if collection empty
if collection.count_documents({}) == 0:
    with open("osm-output.json", "r") as f:
        data = json.load(f)
        nodes = data["nodes"]
    # bulk insert
    result = collection.insert_many(nodes)
    print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
else:
    print(
        f"The collection '{collection_name}' already contains {collection.count_documents({})} documents. No data inserted."
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
Create (or load) new mongoDB collection with project-relevant data
"""
filtered_collection_name = "osm_h2wo"

# check if the collection already exists
if filtered_collection_name in db.list_collection_names():
    print(f"Collection '{filtered_collection_name}' has already been created.")
else:
    print(
        f"Collection '{filtered_collection_name}' hasn't been created yet, will do that now for you :)."
    )

collection_filtered = db[
    filtered_collection_name
]  # load new collection, will be created if not present

# load documents into collection if collection empty
if collection_filtered.count_documents({}) == 0:
    result = collection_filtered.insert_many(filtered_amenities)
    print(
        f"Inserted {len(result.inserted_ids)} documents into '{filtered_collection_name}'."
    )
else:
    print(
        f"The collection '{filtered_collection_name}' already contains {collection_filtered.count_documents({})} documents. No data inserted."
    )
