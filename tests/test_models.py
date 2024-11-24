import random

import pytest
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

import models


@pytest.fixture
def h2wo_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["osm_h2wo"]  # select collection
    return collection


@pytest.fixture
def users_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["users"]  # select collection
    return collection


@pytest.fixture
def dummy_user():
    dummy = {
        "username": "Dummy-User",
        "password_hash": generate_password_hash("password"),
        "email": "dummy@user.com",
        "favourites": [],
    }
    return dummy


def test_get_amenities_wrong_amenity(h2wo_collection, capsys):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="wrong_amenity_name", coordinates_only=False
    )
    captured = capsys.readouterr()
    assert "Invalid amenity_name" in captured.out
    assert len(amenities) == 0


def test_get_amenities_water_all(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="water", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_water_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="water", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) == 3  # only lat, lon, and id


def test_get_amenities_toilets_all(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="toilets", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_toilets_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="toilets", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_bench_all(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="bench", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_bench_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="bench", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_shelter_all(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="shelter", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_shelter_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="shelter", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_waste_basket_all(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="waste_basket", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_waste_basket_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        col=h2wo_collection, amenity_name="waste_basket", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


# def test_email_used_true(users_collection):
#     assert models.email_used(user_col=users_collection, email="demo@user.com")
#
#
# def test_email_used_false(users_collection):
#     assert not models.email_used(user_col=users_collection, email="test@user.com")
#
#
# def test_insert_new_user(users_collection, dummy_user):
#     try:
#         models.insert_new_user(user_col=users_collection, user=dummy_user)
#         assert models.email_used(user_col=users_collection, email=dummy_user["email"])
#     finally:  # delete dummy user again after test
#         users_collection.delete_one({"email": dummy_user["email"]})
#
#
# def test_get_user_exists(users_collection):
#     assert models.get_user(user_col=users_collection, email="demo@user.com")
#
#
# def test_get_user_exists_not(users_collection):
#     assert not models.get_user(user_col=users_collection, email="test@user.com")
