import random

import pytest
from pymongo import MongoClient
import models


@pytest.fixture
def pymongo_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["osm_h2wo"]  # select collection
    return collection


def test_get_water_amenities_all(pymongo_collection):
    amenities = models.get_water_amenities(
        col=pymongo_collection, coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_water_amenities_coordinates_only(pymongo_collection):
    amenities = models.get_water_amenities(
        col=pymongo_collection, coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) == 3  # only lat, lon, and id


def test_get_toilets_all(pymongo_collection):
    amenities = models.get_toilets(col=pymongo_collection, coordinates_only=False)
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_toilets_coordinates_only(pymongo_collection):
    amenities = models.get_toilets(col=pymongo_collection, coordinates_only=True)
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) == 3  # only lat, lon, and id


def test_get_accommodations_all(pymongo_collection):
    amenities = models.get_accommodations(
        col=pymongo_collection, coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_accommodations_coordinates_only(pymongo_collection):
    amenities = models.get_accommodations(col=pymongo_collection, coordinates_only=True)
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) == 3  # only lat, lon, and id
