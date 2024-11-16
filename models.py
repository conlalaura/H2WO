from pymongo.collection import Collection


def get_water_amenities(col: Collection, coordinates_only=False) -> list[dict]:
    """
    Get information for all water related amenities: fountain, water_point, drinking_water, water_tap

    Parameters:
        - collection: mongodb collection of project relevant amenities
        - coordinates_only: choose if only id and coordinates should be returned

    Returns:
    - list: list of dicts, containing information about water related amenities
    """
    # water related amenities
    query = {
        "amenity": {"$in": ["fountain", "water_point", "drinking_water", "water_tap"]}
    }
    # coordinate check
    if coordinates_only:
        keys = {"lat": 1, "lon": 1, "id": 1, "_id": 0}
    else:
        keys = {"_id": 0}
    # filter database
    result = col.find(query, keys)
    # return as list
    return list(result)


def get_toilets(col: Collection, coordinates_only=False) -> list[dict]:
    """
    Get information for all toilets

    Parameters:
        - collection: mongodb collection of project relevant amenities
        - coordinates_only: choose if only id and coordinates should be returned

    Returns:
    - list: list of dicts, containing information about toilets
    """
    # water related amenities
    query = {"amenity": "toilets"}
    # coordinate check
    if coordinates_only:
        keys = {"lat": 1, "lon": 1, "id": 1, "_id": 0}
    else:
        keys = {"_id": 0}
    # filter database
    result = col.find(query, keys)
    # return as list
    return list(result)


def get_accommodations(col: Collection, coordinates_only=False) -> list[dict]:
    """
    Get information for all accommodating amenities: bench, waste_basket, shelter

    Parameters:
        - collection: mongodb collection of project relevant amenities
        - coordinates_only: choose if only id and coordinates should be returned

    Returns:
    - list: list of dicts, containing information about accommodating amenities
    """
    # water related amenities
    query = {"amenity": {"$in": ["bench", "waste_basket", "shelter"]}}
    # coordinate check
    if coordinates_only:
        keys = {"lat": 1, "lon": 1, "id": 1, "_id": 0}
    else:
        keys = {"_id": 0}
    # filter database
    result = col.find(query, keys)
    # return as list
    return list(result)
