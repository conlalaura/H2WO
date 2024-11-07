import pymongo
import json

client = pymongo.MongoClient(host="localhost", port=27017)
db = client["osm"]  # select db
collection_name = "osm"

"""
this section creates a collection with all OpenSteetMap data
"""
# check if the collection already exists
if collection_name not in db.list_collection_names():
    collection = db[collection_name]

    # read the json data only if the collection doesn't exist
    with open("osm-output.json", "r") as f:
        data = json.load(f)
        nodes = data["nodes"]

    # bulk insert
    result = collection.insert_many(nodes)
    print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}.")
else:
    print(f"The collection '{collection_name}' already exists. No data inserted.")

"""
this section selects only project-relevant data from the OpenSteetMap 
"""
# load collection
collection = db[collection_name]

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
this section saves the project-relevant data into a new mongoDB collection 
"""
filtered_collection_name = "osm_h2wo"

# check if the collection already exists
if filtered_collection_name not in db.list_collection_names():
    collection = db[filtered_collection_name]
    result = collection.insert_many(filtered_amenities)
    print(
        f"Inserted {len(result.inserted_ids)} documents into {filtered_collection_name}."
    )
else:
    print(
        f"The collection '{filtered_collection_name}' already exists. No data inserted."
    )
