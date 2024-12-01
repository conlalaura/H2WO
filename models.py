from pymongo.collection import Collection
from dataclasses import asdict
from lib.Review import Review


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


def get_chart_data(osm_col: Collection) -> list[dict]:
    """
    Collects data for the amenity statistics
    :param osm_col: mongodb collection of project relevant amenities
    :return: list of dicts with counts for every amenity
    """
    pipeline = [
        {"$group": {"_id": "$amenity", "count": {"$count": {}}}},
        {"$sort": {"count": -1}},  # Optional: Sort by count in descending order
    ]

    result = osm_col.aggregate(pipeline)

    return list(result)


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
