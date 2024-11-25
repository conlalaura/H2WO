from dataclasses import asdict

from pymongo.collection import Collection
from pymongo.database import Database
from lib.Review import Review
from pathlib import Path
import pymongo
import random
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_and_load_collection(collection_name: str, database: Database) -> Collection:
    """
    Function crates a collection in the database if it's not present yet or returns the already existing collection.
    :param collection_name: to be created and loaded from the database    .
    :param database:  to search and load the collection from.
    :return: collection with name "collection_name" from database
    """
    # check if the collection already exists
    if collection_name in database.list_collection_names():
        print(f"Collection '{collection_name}' has already been created.")
    else:
        print(
            f"Collection '{collection_name}' hasn't been created yet, will do that now for you"
            + " \U0001F917"
        )
    return database[
        collection_name
    ]  # load and return collection, will be created if not present


def insert_if_empty(col: Collection, documents: list[dict]) -> None:
    """
    Inserts the passed documents into the collection if the collection is empty.
    :param col: to be filled with passed documents.
    :param documents: list of documents to be loaded into the collection.
    :return: None
    """
    if col.count_documents({}) == 0:
        # bulk insert
        col.insert_many(documents)
        print(f"Inserted {len(documents)} documents into '{col.name}'.")
    else:
        print(
            f"The collection '{col.name}' already contains {col.count_documents({})} documents. No data inserted."
        )


def get_project_amenities(
    col: Collection, amenity_name: str, amenity_keys: dict, special_keys=None
) -> list[dict]:
    """
    Searches the osm collection for a given amenity and keys
    :param col: OSM Collection
    :param amenity_name: Amenity to search in the collection
    :param amenity_keys: Keys associated with the amenity
    :param special_keys: Key to artificially add to the amenity (e.g. "drinking_water": "yes" for water_point)
    :return: List with documents that satisfy the amenity and key query
    """
    if special_keys is None:
        special_keys = {}
    query = {"amenity": amenity_name}
    results = col.find(query, amenity_keys)
    results = list(results)  # convert curser
    if special_keys:
        for key, value in special_keys.items():
            for i in range(len(results)):
                results[i][key] = value
    for i in range(len(results)):
        results[i]["lat"] = convert_to_float(results[i]["lat"])
        results[i]["lon"] = convert_to_float(results[i]["lon"])
    return list(results)


def convert_to_float(input_string: str) -> float:
    """
    Converts a string input to float, used for lat/lon keys of the amenities
    :param input_string: a string like e.g. "47.12345"
    :return: float
    """
    try:
        return float(input_string)
    except ValueError as e:
        raise ValueError(
            f"Invalid input for conversion to float: '{input_string}'"
        ) from e


def insert_dummy_reviews(
    col: Collection,
    n=500,
    bounding_box_lower_left=(47.449, 8.655),
    bounding_box_upper_right=(47.549, 8.811),
) -> None:
    """
    Inserts Dummy reviews into the project collection. Useful for demonstration purposes. By default, Witherthur Area.
    :param col: Collection to insert dummy reviews
    :param n: number of amenities to add dummy review
    :param bounding_box_lower_left: lat/lon of the bounding box lower left corner, default is Nürensdorf
    :param bounding_box_upper_right: lat/lon of the bounding box upper right corner default is Wiesendangen
    :return: None
    """
    # use flag to check if dummy-reviews have already been added
    if col.find_one({"dummy_reviews_flag": {"$exists": True}}):
        print("Dummy-Reviews have already been added. You're good to go!")
    else:
        print(
            f"Will add now {n} dummy-reviews to random amenities in the Winterthur-Area."
        )
        print(
            "Updating documents takes more time so please bare with me" + " \U0001F917"
        )

        # Filter documents with valid lat and lon values (default is Winterthur)
        query = {
            "lat": {
                "$gte": bounding_box_lower_left[0],
                "$lte": bounding_box_upper_right[0],
            },
            "lon": {
                "$gte": bounding_box_lower_left[1],
                "$lte": bounding_box_upper_right[1],
            },
        }

        pipeline = [
            {"$match": query},
            {
                "$sample": {"size": n}
            },  # Randomly select n documents to add dummy reviews
        ]

        random_amenities = list(col.aggregate(pipeline))
        review = Review(
            username="Dummy",
            rating=random.randint(1, 5),
            review="This is a dummy-review for the project demonstration.",
        )

        for am in random_amenities:
            filter_query = {"id": am["id"]}
            update_query = {"$set": {"reviews": [asdict(review)]}}

            col.update_one(filter_query, update_query)

        # insert flag document to verify that dummy reviews have been inserted
        col.insert_one({"dummy_reviews_flag": None})

        print("Randomly added 500 dummy-reviews to amenities in the Winterthur-Area!")


if __name__ == "__main__":
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    osm_collection_name = "osm_all_amenities"

    """
    Create and load collection with all OpenSteetMap data
    """
    osm_collection = create_and_load_collection(
        collection_name=osm_collection_name, database=db
    )

    with open(Path(__file__).parent / "osm-output.json", "r") as f:
        data = json.load(f)
        nodes = data["nodes"]

    # load documents into collection if collection is empty
    insert_if_empty(col=osm_collection, documents=nodes)

    """
    Select only project-relevant data from the OpenSteetMap 
    """
    # keys used for all amenities
    common_keys = {
        "name": 1,
        "amenity": 1,
        "lat": 1,
        "lon": 1,
        "id": 1,
    }
    # amenity-specific keys
    all_amenity_keys = {
        "fountain": {
            **common_keys,
            "drinking_water": 1,
        },
        "water_point": {
            **common_keys,
        },
        "drinking_water": {
            **common_keys,
            "wheelchair": 1,
            "bottle": 1,
            "seasonal": 1,
        },
        "toilets": {
            **common_keys,
            "fee": 1,
            "wheelchair": 1,
            "changing_table": 1,
            "male": 1,
            "female": 1,
            "unisex": 1,
        },
        "bench": {
            **common_keys,
            "seats": 1,
            "covered": 1,
        },
        "water_tap": {
            **common_keys,
        },
        "waste_basket": {
            **common_keys,
            "waste": 1,
        },
        "shelter": {
            **common_keys,
            "bench": 1,
            "bin": 1,
            "picnic_table": 1,
            "table": 1,
            "drinking_water": 1,
        },
    }

    filtered_amenities = []

    for amenity, keys in all_amenity_keys.items():
        if amenity in ["water_point", "drinking_water"]:
            special_key = {"drinking_water": "yes"}
        else:
            special_key = {}
        docs = get_project_amenities(
            col=osm_collection,
            amenity_name=amenity,
            amenity_keys=keys,
            special_keys=special_key,
        )
        for doc in docs:
            filtered_amenities.append(doc)

    """
    Create or load new mongoDB collection with project-relevant data
    """
    filtered_collection_name = "osm_h2wo"
    h2wo_collection = create_and_load_collection(
        collection_name=filtered_collection_name, database=db
    )
    # load documents into collection if collection empty
    insert_if_empty(col=h2wo_collection, documents=filtered_amenities)

    """
    Insert dummy reviews for 500 random amenities in Winterthur for (used for demo)
    """
    insert_dummy_reviews(col=h2wo_collection)
