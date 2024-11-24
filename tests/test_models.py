import random
import pytest
from pymongo import MongoClient
import models


@pytest.fixture
def h2wo_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["osm_h2wo"]  # select collection
    return collection


@pytest.fixture
def dummy_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["dummy"]  # select collection
    return collection


@pytest.fixture()
def dummy_review():
    review = {
        "username": "dummy",
        "rating": 5,
        "review": "Pytest",
    }
    return review


def test_get_amenities_wrong_amenity(h2wo_collection, capsys):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection,
        amenity_name="wrong_amenity_name",
        coordinates_only=False,
    )
    captured = capsys.readouterr()
    assert "Invalid amenity_name" in captured.out
    assert len(amenities) == 0


def test_get_amenities_water_all(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="water", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_water_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="water", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) == 3  # only lat, lon, and id


def test_get_amenities_toilets_all(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="toilets", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_toilets_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="toilets", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_bench_all(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="bench", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_bench_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="bench", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_shelter_all(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="shelter", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_shelter_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="shelter", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_waste_basket_all(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="waste_basket", coordinates_only=False
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_get_amenities_waste_basket_coordinates_only(h2wo_collection):
    amenities = models.get_amenities(
        amenity_col=h2wo_collection, amenity_name="waste_basket", coordinates_only=True
    )
    # use 10 random indexes to test
    random.seed(19)
    random_indexes = random.sample(range(len(amenities)), 10)
    for index in random_indexes:
        assert len(amenities[index]) >= 3


def test_insert_and_get_review(dummy_collection, dummy_review):
    amenity_id = "TestId"
    n = 3
    try:
        dummy_collection.insert_one({"id": amenity_id})
        for i in range(n):
            models.insert_review(
                amenity_col=dummy_collection, amenity_id=amenity_id, doc=dummy_review
            )
        result = models.get_reviews(amenity_col=dummy_collection, amenity_id=amenity_id)
        assert len(result) == n
    finally:
        dummy_collection.delete_one({"id": amenity_id})
