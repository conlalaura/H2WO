from pymongo.collection import Collection
from dataclasses import asdict
from lib.Review import Review
from data.mongodb_loader import get_common_keys, get_all_amenity_keys


def get_amenities(
    osm_col: Collection, amenity_name: str, coordinates_only=False
) -> list[dict]:
    """
    :param osm_col: mongodb collection of project relevant amenities
    :param amenity_name: can be
        - water (fountain, water_point, drinking_water, water_tap)
        - toilets
        - bench
        - shelter
        - waste_basket
    :param coordinates_only: choose if only id and coordinates should be returned
    :return: list of amenities
    """
    # Validate the amenity_name
    allowed_amenities = ["water", "toilets", "bench", "shelter", "waste_basket"]
    if amenity_name not in allowed_amenities:
        print(
            f"Invalid amenity_name: {amenity_name}. Allowed values are: {allowed_amenities}"
        )
        return []
    # multiple amenities for water
    if amenity_name == "water":
        query = {
            "amenity": {
                "$in": ["fountain", "water_point", "drinking_water", "water_tap"]
            }
        }
    else:
        query = {"amenity": amenity_name}
    # coordinate check
    if coordinates_only:
        keys = {"lat": 1, "lon": 1, "id": 1, "_id": 0}
    else:
        keys = {"_id": 0}  # keeps all keys except _id
    # filter database
    result = osm_col.find(query, keys)
    # return as list
    return list(result)


def get_homepage_data(osm_col: Collection) -> list[dict]:
    """
    Collects data for the amenity statistics
    :param osm_col: mongodb collection of project relevant amenities
    :return: list of dicts with counts for toilets and watersources
    """
    pipeline = [
        # match docs that have an amenity key
        {
            "$match": {
                "amenity": {
                    "$in": [
                        "water_point",
                        "drinking_water",
                        "water_tap",
                        "fountain",
                        "toilets",
                    ]
                }
            }
        },
        # collect water-related amenities to "watersources"
        {
            "$set": {
                "amenity": {
                    "$cond": {
                        "if": {
                            "$in": [
                                "$amenity",
                                [
                                    "water_point",
                                    "drinking_water",
                                    "water_tap",
                                    "fountain",
                                ],
                            ]
                        },
                        "then": "watersources",
                        "else": "$amenity",
                    }
                }
            }
        },
        # Group by the mapped amenity categories
        {"$group": {"_id": "$amenity", "count": {"$count": {}}}},
    ]

    result = osm_col.aggregate(pipeline)

    return list(result)


def get_toilet_statistics_data(amenity_col: Collection) -> list[dict]:
    """
    Returns statistics about toilet facilities
    :param amenity_col: mongodb collection of project relevant amenities
    :return: percentage yes/no of toilet accommodations
    """
    pipeline = [
        {"$match": {"amenity": "toilets"}},
        # Dynamically rename fee to free
        {"$addFields": {"free": "$fee"}},
        {
            "$project": {
                "free_yes": {"$cond": [{"$eq": ["$free", "no"]}, 1, 0]},
                "free_no": {"$cond": [{"$eq": ["$free", "yes"]}, 1, 0]},
                "wheelchair_yes": {"$cond": [{"$eq": ["$wheelchair", "yes"]}, 1, 0]},
                "wheelchair_no": {"$cond": [{"$eq": ["$wheelchair", "no"]}, 1, 0]},
                "changing_table_yes": {
                    "$cond": [{"$eq": ["$changing_table", "yes"]}, 1, 0]
                },
                "changing_table_no": {
                    "$cond": [{"$eq": ["$changing_table", "no"]}, 1, 0]
                },
                "male_yes": {"$cond": [{"$eq": ["$male", "yes"]}, 1, 0]},
                "male_no": {"$cond": [{"$eq": ["$male", "no"]}, 1, 0]},
                "female_yes": {"$cond": [{"$eq": ["$female", "yes"]}, 1, 0]},
                "female_no": {"$cond": [{"$eq": ["$female", "no"]}, 1, 0]},
                "unisex_yes": {"$cond": [{"$eq": ["$unisex", "yes"]}, 1, 0]},
                "unisex_no": {"$cond": [{"$eq": ["$unisex", "no"]}, 1, 0]},
            }
        },
        {
            "$group": {
                "_id": None,
                "total": {"$sum": 1},
                "free_yes": {"$sum": "$free_yes"},
                "free_no": {"$sum": "$free_no"},
                "wheelchair_yes": {"$sum": "$wheelchair_yes"},
                "wheelchair_no": {"$sum": "$wheelchair_no"},
                "changing_table_yes": {"$sum": "$changing_table_yes"},
                "changing_table_no": {"$sum": "$changing_table_no"},
                "male_yes": {"$sum": "$male_yes"},
                "male_no": {"$sum": "$male_no"},
                "female_yes": {"$sum": "$female_yes"},
                "female_no": {"$sum": "$female_no"},
                "unisex_yes": {"$sum": "$unisex_yes"},
                "unisex_no": {"$sum": "$unisex_no"},
            }
        },
        {
            "$project": {
                "fields": [
                    {
                        "key": "free",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$free_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$free_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                    {
                        "key": "wheelchair",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$wheelchair_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$wheelchair_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                    {
                        "key": "changing_table",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$changing_table_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$changing_table_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                    {
                        "key": "male",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$male_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$male_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                    {
                        "key": "female",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$female_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$female_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                    {
                        "key": "unisex",
                        "yes": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$unisex_yes", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                        "no": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$unisex_no", "$total"]},
                                        100,
                                    ]
                                },
                                1,
                            ]
                        },
                    },
                ]
            }
        },
        {"$unwind": "$fields"},
        {"$sort": {"fields.yes": -1}},
    ]
    return list(amenity_col.aggregate(pipeline))


def get_sparsity_statistics_data(amenity_col: Collection) -> list[dict]:
    """
    Returns statistics about the sparsity of oms data
    :param amenity_col: mongodb collection of project relevant amenities
    :return: average percentage of available keys per amenity type
    """
    common_keys = get_common_keys()
    all_amenity_keys = get_all_amenity_keys(common_keys)

    expected_key_number = {
        key: len(value) - len(common_keys)
        for (key, value) in all_amenity_keys.items()
        if len(value) - len(common_keys) != 0
    }

    result = []

    # Iterate over each amenity type and calculate the metric
    for amenity_name, expected_number in expected_key_number.items():
        query = {"amenity": amenity_name}
        keys = {
            "_id": 0,
            "name": 0,
            "amenity": 0,
            "lat": 0,
            "lon": 0,
            "id": 0,
        }  # don't keep mongodb id and common keys
        res = amenity_col.find(query, keys)
        fractions_of_keys = [len(doc) / expected_number * 100 for doc in res]
        fraction = sum(fractions_of_keys) / len(fractions_of_keys)
        result.append({amenity_name: round(fraction, 1)})

    return result


def insert_review(amenity_col: Collection, amenity_id: str, review: Review) -> None:
    """
    Inserts a new review (doc) into the review collections
    :param amenity_col: mongodb collection of project relevant amenities
    :param amenity_id: update reviews for this amenity id
    :param review: review as a Review (dataclass) including username, rating and review
    :return: None
    """
    filter_query = {"id": amenity_id}
    update_query = {"$push": {"reviews": asdict(review)}}
    amenity_col.update_one(filter_query, update_query)


def get_reviews(amenity_col: Collection, amenity_id: str) -> list[dict]:
    """
    Gets all reviews associated with the passed amenity_id
    :param amenity_col: mongodb collection of project relevant amenities
    :param amenity_id: get reviews for this amenity id
    :return: list of reviews for this amenity
    """
    result = amenity_col.find_one({"id": amenity_id})
    return result.get("reviews", [])
