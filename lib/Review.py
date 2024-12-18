from dataclasses import dataclass


@dataclass
class Review:
    """
    Class representing a review for a specific amenity

    Attributes:
        username (str): The name of the user leaving the review.
        rating (int): The rating given by the user, ranging from 1 to 5.
        comment (str): The user's comment or feedback.
    """

    username: str
    rating: int
    comment: str

    def __post_init__(self):
        """
        Validates that the rating is within the acceptable range (1 to 5).
        Raises a ValueError if the rating is outside this range.
        """
        if not (1 <= self.rating <= 5):
            raise ValueError(f"Rating must be between 1 and 5. Got: {self.rating}")
