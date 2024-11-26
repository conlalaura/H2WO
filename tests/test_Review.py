import pytest

from lib.Review import Review


def test_review():
    username = "ABC"
    rating = 5
    comment = "DEF"
    test = Review(username=username, rating=rating, comment=comment)
    assert test.username == username
    assert isinstance(test.username, str)
    assert test.rating == rating
    assert isinstance(test.rating, int)
    assert test.comment == comment
    assert isinstance(test.comment, str)


def test_review_wrong_rating():
    username = "ABC"
    rating = 50
    review = "DEF"
    with pytest.raises(ValueError, match="Rating must be between 1 and 5. Got:"):
        test = Review(username=username, rating=rating, comment=review)
