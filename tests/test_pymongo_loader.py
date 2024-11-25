import json
from pathlib import Path

import pytest
from pymongo import MongoClient
import data.mongodb_loader as mongodb_loader
from pymongo.collection import Collection


@pytest.fixture
def dummy_document():
    return {"name": "Test"}


@pytest.fixture
def test_database():
    client = MongoClient(host="localhost", port=27017)
    db = client["test_db"]  # select db
    yield db
    client.drop_database("test_db")


@pytest.fixture
def test_collection_generic(test_database, dummy_document):
    test_collection_name = "test"
    test_collection = mongodb_loader.create_and_load_collection(
        collection_name=test_collection_name, database=test_database
    )
    test_collection.insert_one(dummy_document)
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


@pytest.fixture
def amenity_keys():
    common_keys = {
        "name": 1,
        "amenity": 1,
        "lat": 1,
        "lon": 1,
        "id": 1,
    }
    # amenity-specific keys
    amenity_keys = {
        "fountain": {
            **common_keys,
            "drinking_water": 1,
        },
        "water_point": {
            **common_keys,
        },
    }
    return amenity_keys


def test_create_and_load_collection_creates_when_absent(
    test_database, dummy_document, capsys
):
    col_name = "function_test"
    col = mongodb_loader.create_and_load_collection(
        collection_name=col_name, database=test_database
    )
    captured = capsys.readouterr()
    col.insert_one(dummy_document)
    assert "hasn't been created yet" in captured.out
    assert col_name in test_database.list_collection_names()
    assert isinstance(col, Collection)


def test_create_and_load_collection_returns_existing(
    test_database, test_collection_generic, capsys
):
    col = mongodb_loader.create_and_load_collection(
        collection_name=test_collection_generic.name, database=test_database
    )
    captured = capsys.readouterr()
    assert "has already been created" in captured.out
    assert test_collection_generic.name in test_database.list_collection_names()
    assert isinstance(col, Collection)


def test_insert_if_empty_collection_empty(test_database, dummy_document, capsys):
    col_name = "function_test"
    col = mongodb_loader.create_and_load_collection(
        collection_name=col_name, database=test_database
    )
    mongodb_loader.insert_if_empty(col=col, documents=[dummy_document])
    captured = capsys.readouterr()
    assert "Inserted" in captured.out


def test_insert_if_empty_collection_filled(
    test_collection_generic, dummy_document, capsys
):
    mongodb_loader.insert_if_empty(
        col=test_collection_generic, documents=[dummy_document]
    )
    captured = capsys.readouterr()
    assert "already contains" in captured.out


def test_get_project_amenities_without_special_keys(test_collection_h2wo, amenity_keys):
    amenity = "fountain"
    amenity_keys = amenity_keys[amenity]
    result = mongodb_loader.get_project_amenities(
        col=test_collection_h2wo, amenity_name=amenity, amenity_keys=amenity_keys
    )
    assert len(result) == 1
    assert result[0]["amenity"] == amenity


def test_get_project_amenities_with_special_keys(test_collection_h2wo, amenity_keys):
    amenity = "water_point"
    amenity_keys = amenity_keys[amenity]
    result = mongodb_loader.get_project_amenities(
        col=test_collection_h2wo,
        amenity_name=amenity,
        amenity_keys=amenity_keys,
        special_keys={"drinking_water": "yes"},
    )
    assert len(result) == 1
    assert result[0]["amenity"] == amenity


def test_convert_to_float_successful():
    input_string = "1234"
    res = mongodb_loader.convert_to_float(input_string=input_string)
    assert isinstance(res, float)


def test_convert_to_float_error():
    with pytest.raises(ValueError, match="Invalid input for conversion to float"):
        mongodb_loader.convert_to_float("invalid_string")


def test_insert_dummy_reviews(test_collection_h2wo, capsys):
    res1 = test_collection_h2wo.find_one({"dummy_reviews_flag": {"$exists": True}})
    assert not res1
    n = 1
    mongodb_loader.insert_dummy_reviews(col=test_collection_h2wo, n=n)
    res2 = test_collection_h2wo.find_one({"dummy_reviews_flag": {"$exists": True}})
    captured = capsys.readouterr()
    assert res2
    assert f"Will add now {n} dummy-reviews" in captured.out
