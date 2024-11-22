from pymongo.collection import Collection

def get_amenities(
    col: Collection, amenity_name: str, coordinates_only=False
) -> list[dict]:
    """
    :param col: mongodb collection of project relevant amenities
    :param amenity_name: can be
        - water (fountain, water_point, drinking_water, water_tap)
        - toilets
        - bench
        - shelter
        - waste_basket
    :param coordinates_only: choose if only id and coordinates should be returned
    :return:
    """
    # Validate the amenity_name
    allowed_amenities = ["water", "toilets", "bench", "shelter", "waste_basket"]
    if amenity_name not in allowed_amenities:
        print(f"Invalid amenity_name: {amenity_name}. Allowed values are: {allowed_amenities}")
        return []
    # multiple amenities fore water
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
        keys = {"lat": 1, "lon": 1, "_id": 1}
    else:
        keys = None  # keeps all keys
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
