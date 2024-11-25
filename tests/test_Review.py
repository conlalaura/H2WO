import pytest

from lib.Review import Review


def test_review():
    username = "ABC"
    rating = 5
    review = "DEF"
    test = Review(username=username, rating=rating, review=review)
    assert test.username == username
    assert isinstance(username, str)
    assert test.rating == rating
    assert isinstance(rating, int)
    assert test.review == review
    assert isinstance(review, str)


def test_review_wrong_rating():
    username = "ABC"
    rating = 50
    review = "DEF"
    with pytest.raises(ValueError, match="Rating must be between 1 and 5. Got:"):
        test = Review(username=username, rating=rating, review=review)
