from pymongo import MongoClient
from data import mongodb_loader
from lib.Review import Review
from pathlib import Path
import pytest
import models
import json


@pytest.fixture
def test_database():
    client = MongoClient(host="localhost", port=27017)
    db = client["test_db"]  # select db
    yield db
    client.drop_database("test_db")


@pytest.fixture
def test_collection_generic(test_database):
    test_collection_name = "test"
    test_collection = mongodb_loader.create_and_load_collection(
        collection_name=test_collection_name, database=test_database
    )
    yield test_collection
    test_collection.drop()


@pytest.fixture
def test_collection_h2wo(test_database):
    test_collection_name = "test"
    with open(Path(__file__).parent.parent / "data/dummy_document.json", "r") as f:
        documents = json.load(f)
    test_collection = mongodb_loader.create_and_load_collection(
        collection_name=test_collection_name, database=test_database
    )
    mongodb_loader.insert_if_empty(col=test_collection, documents=documents)
    yield test_collection
    test_collection.drop()


@pytest.fixture()
def test_review():
    review = Review(
        username="Test-User",
        rating=5,
        comment="This is a test-review for the testing.",
    )
    return review


def test_get_amenities_wrong_amenity(test_collection_h2wo, capsys):
    amenities = models.get_amenities(
        osm_col=test_collection_h2wo, amenity_name="wrong_amenity_name"
    )
    captured = capsys.readouterr()
    assert "Invalid amenity_name" in captured.out
    assert len(amenities) == 0


def test_get_amenities_water_all(test_collection_h2wo):
    amenities = models.get_amenities(osm_col=test_collection_h2wo, amenity_name="water")
    for amenity in amenities:
        assert len(amenity) >= 3


def test_get_amenities_toilets_all(test_collection_h2wo):
    amenities = models.get_amenities(
        osm_col=test_collection_h2wo, amenity_name="toilets"
    )
    for amenity in amenities:
        assert len(amenity) >= 3


def test_get_amenities_bench_all(test_collection_h2wo):
    amenities = models.get_amenities(osm_col=test_collection_h2wo, amenity_name="bench")
    for amenity in amenities:
        assert len(amenity) >= 3


def test_get_amenities_shelter_all(test_collection_h2wo):
    amenities = models.get_amenities(
        osm_col=test_collection_h2wo, amenity_name="shelter"
    )
    for amenity in amenities:
        assert len(amenity) >= 3


def test_get_amenities_waste_basket_all(test_collection_h2wo):
    amenities = models.get_amenities(
        osm_col=test_collection_h2wo, amenity_name="waste_basket"
    )
    for amenity in amenities:
        assert len(amenity) >= 3


def test_insert_and_get_review(test_collection_generic, test_review):
    amenity_id = "TestId"
    n = 10
    test_collection_generic.insert_one({"id": amenity_id})
    for i in range(n):
        models.insert_review(
            amenity_col=test_collection_generic,
            amenity_id=amenity_id,
            review=test_review,
        )
    result = models.get_reviews(
        amenity_col=test_collection_generic, amenity_id=amenity_id
    )
    assert len(result) == n


def test_get_homepage_data(test_collection_h2wo):
    count_data = models.get_homepage_data(osm_col=test_collection_h2wo)
    data_dict = {item["_id"]: item["count"] for item in count_data}
    assert len(count_data) == 2
    assert "watersources" in data_dict.keys()
    assert "toilets" in data_dict.keys()
