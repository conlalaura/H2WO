from pymongo.collection import Collection
import pymongo
import random
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
            f"Collection '{collection_name}' hasn't been created yet, will do that now for you" + " \U0001F917"
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
            for result in results:
                result["drinking_water"] = (
                    "yes"  # Add the drinking_water tag, by definition always yes for this amenity
                )
                filtered_amenities.append(
                    result
                )  # append individual dicts/jsons to filtered_amenities

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
            for result in results:
                result["drinking_water"] = (
                    "yes"  # Add the drinking_water tag, by definition always yes for this amenity
                )
                filtered_amenities.append(
                    result
                )  # append individual dicts/jsons to filtered_amenities

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
    Convert lat/lon values to float
    """
    for i in range(len(filtered_amenities)):
        filtered_amenities[i]["lat"] = float(filtered_amenities[i]["lat"])
        filtered_amenities[i]["lon"] = float(filtered_amenities[i]["lon"])

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
    Select 500 amenities in Winterthur for random reviews (used for demo)
    """
    print("Will add now 500 dummy-reviews to random amenities in the Winterthur-Area.")
    print("Updating documents takes more time so please bare with me" + " \U0001F917")
    lower_left = (47.449, 8.655)  # approx. lat/lon Nürensdorf
    upper_right = (47.549, 8.811)  # approx. lat/lon Wiesendangen

    # Filter for documents with valid lat and lon values
    query = {
        "lat": {
            "$gte": lower_left[0],
            "$lte": upper_right[0],
        },  # valid lat for Winterthur area
        "lon": {
            "$gte": lower_left[1],
            "$lte": upper_right[1],
        },  # valid lon for Winterthur area
    }

    pipeline = [
        {"$match": query},
        {"$sample": {"size": 500}},  # Randomly select 500 documents
    ]

    random_amenities = list(h2wo_collection.aggregate(pipeline))

    for amenity in random_amenities:
        filter_query = {"id": amenity["id"]}
        update_query = {"$set": {"reviews": [{
            "username": amenity["id"],
            "rating": random.randint(1, 5),
            "review": "This is a dummy-review for the project demonstration.",
        }]}}

        h2wo_collection.update_one(filter_query, update_query)
    print("Randomly added 500 dummy-reviews to amenities in the Winterthur-Area!")

    # """
    # Create or load new mongoDB collection with review
    # """
    # review_collection_name = "reviews"
    # review_collection = check_or_create_collection(
    #     collection_name=review_collection_name, database=db
    # )
    # insert_if_empty(col=review_collection, documents=review_amenities)
