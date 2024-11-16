from pymongo.collection import Collection


def get_water_amenities(col: Collection, coordinates_only=False) -> list[dict]:
    """
    Get information for all water related amenities: fountain, water_point, drinking_water, water_tap

    :param col: mongodb collection of project relevant amenities
    :param coordinates_only: choose if only id and coordinates should be returned

    :return:  list of dicts, containing information about water related amenities
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

    :param col: mongodb collection of project relevant amenities
    :param coordinates_only: choose if only id and coordinates should be returned

    :return:  list of dicts, containing information about toilets
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

    :param col: mongodb collection of project relevant amenities
    :param coordinates_only: choose if only id and coordinates should be returned

    :return:  list of dicts, containing information about accommodating amenities
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


def email_used(user_col: Collection, email: str) -> bool:
    """
    Checks if the provided email has already been registered as user

    :param user_col: mongodb collection of registered users
    :param email: email to be used for registration

    :return: bool
    """
    return user_col.find_one({"email": email})


def insert_new_user(user_col: Collection, user: dict) -> None:
    """
    Adds a new user to the users collection

    :param user_col: mongodb collection of registered users
    :param user: dictionary with user information (username, email, hashed password, empty favourites list)
    :return: None
    """
    if not email_used(user_col, user["email"]):
        user_col.insert_one(user)


def get_user(user_col: Collection, email: str) -> dict:
    """
    Gets the user information from the provided database and email

    :param user_col: mongodb collection of registered users
    :param email: email of the user
    :return: dictionary with user information (username, email, hashed password, empty favourites list)
    """
    return user_col.find_one({"email": email}) if email_used(user_col, email) else None
