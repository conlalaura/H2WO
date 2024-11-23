import pytest
from pymongo import MongoClient

import data.mongodb_loader as mongodb_loader


@pytest.fixture
def database():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    return db


@pytest.fixture
def h2wo_collection():
    client = MongoClient(host="localhost", port=27017)
    db = client["osm"]  # select db
    collection = db["osm_h2wo"]  # select collection
    return collection


@pytest.fixture
def dummy_document():
    return {"name": "Test"}


def test_check_or_create_collection_create(database, dummy_document, capsys):
    try:
        test_collection_name = "test"
        test_collection = mongodb_loader.check_or_create_collection(
            collection_name=test_collection_name, database=database
        )
        # must insert data, otherwise collection doesn't exist
        test_collection.insert_one(dummy_document)
        captured = capsys.readouterr()
        assert "hasn't been created yet" in captured.out
        assert test_collection_name in database.list_collection_names()
    finally:
        test_collection.drop()


def test_check_or_create_collection_exists(database, h2wo_collection, capsys):
    mongodb_loader.check_or_create_collection(
        collection_name=h2wo_collection.name, database=database
    )
    captured = capsys.readouterr()
    assert "has already been created" in captured.out
    assert h2wo_collection.name in database.list_collection_names()


def test_insert_if_empty_insert(database, dummy_document, capsys):
    try:
        test_collection_name = "test"
        test_collection = mongodb_loader.check_or_create_collection(
            collection_name=test_collection_name, database=database
        )
        mongodb_loader.insert_if_empty(col=test_collection, documents=[dummy_document])
        captured = capsys.readouterr()
        assert "Inserted" in captured.out
        assert "documents into" in captured.out
    finally:
        test_collection.drop()


def test_insert_if_empty_no_insert(dummy_document, h2wo_collection, capsys):
    mongodb_loader.insert_if_empty(col=h2wo_collection, documents=dummy_document)
    captured = capsys.readouterr()
    assert "already contains" in captured.out
    assert "No data inserted" in captured.out
